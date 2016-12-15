import statistics

import facebook
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Count
from django.template.defaultfilters import title

from graph import models as graph_models


def get_title(field_name):
    field_words = field_name.replace('_', ' ')
    return title(field_words)

def _get_statistics_value(values, method_name, num_values_required=1):
    value = None
    if len(values) >= num_values_required:
        value = method_name(values)
    return value


def get_mean(values):
    mean = _get_statistics_value(values, statistics.mean)
    if mean:
        mean = round(mean, 1)
    return mean


def get_median(values):
    return _get_statistics_value(values, statistics.median)


def get_mode(values):
    try:
        mode = _get_statistics_value(values, statistics.mode)
    except statistics.StatisticsError:
        mode = 'No distinct mode found'
    return mode


def _convert_to_date(values):
    return [[value[0].date(), value[1]] for value in values]


def posts_by_time_increment(posts, extra_text):
    posts = posts.extra({'created': extra_text})
    posts = posts.values('created').annotate(total=Count('id')).order_by('created')
    posts = posts.values_list('created', 'total')
    return posts


def posts_by_day(posts):
    return posts_by_time_increment(posts, "date(created_time)")


def posts_by_month(posts):
    posts = posts_by_time_increment(posts, "date_trunc('month', created_time)")
    return _convert_to_date(posts)


def posts_by_year(posts):
    posts = posts_by_time_increment(posts, "date_trunc('year', created_time)")
    return _convert_to_date(posts)


def comments_by_post(comments):
    comments = comments.values('post').annotate(total=Count('id')).order_by('total')
    comments = comments.values_list('post', 'total')
    return comments


def retrieve_facebook_posts(user=None, retrieve_all=False, ignore_errors=False):
    social_accounts = SocialAccount.objects.filter(provider="facebook")
    if user:
        social_accounts = social_accounts.filter(user=user)

    for social_account in social_accounts:
        access_token = social_account.socialtoken_set.all()[0].token
        version = settings.FACEBOOK_API_VERSION
        graph_api = facebook.GraphAPI(access_token=access_token, version=version)
        request_path = 'me/posts/'
        try:
            posts = graph_api.request(request_path)
        except facebook.GraphAPIError as e:
            print('Unable to retrieve posts for {}: {}'.format(social_account, e))
            if not ignore_errors:
                raise e
            continue

        while 'data' in posts:
            for post_data in posts['data']:
                post_data['user'] = social_account.user
                try:
                    post = graph_models.Post(**post_data)
                    post.save()

                    try:
                        attachments = graph_api.request('%s/attachments/' % post_data['id'])
                        for attachment_data in attachments['data']:
                            attachment_data['post'] = post
                            attachment = graph_models.Attachment(**attachment_data)
                            attachment.save()
                            # Only save first attachment, if it exists
                            break
                    except Exception as e:
                        if not ignore_errors:
                            raise e

                    try:
                        comments = graph_api.request('%s/comments/' % post_data['id'])
                        for comment_data in comments['data']:
                            comment_data['post'] = post
                            comment_data['from_json'] = comment_data.pop('from')
                            comment = graph_models.Comment(**comment_data)
                            comment.save()
                            replies = graph_api.request('%s/comments/' % comment_data['id'])
                            for reply_data in replies['data']:
                                reply_data['post'] = post
                                reply_data['comment'] = comment
                                reply_data['from_json'] = reply_data.pop('from')
                                reply = graph_models.Comment(**reply_data)
                                reply.save()
                    except Exception as e:
                        if not ignore_errors:
                            raise e

                except IntegrityError as e:
                    if str(e).find('duplicate key value') >= 0:
                        if not ignore_errors:
                            posts = {}
                            break
                    raise e
                except Exception as e:
                    print(request_path)
                    print(post_data)
                    raise e

            if not retrieve_all or not posts:
                break

            next_page = posts.get('paging', {}).get('next')
            if next_page:
                request_path = 'me/posts?%s' % next_page.split('?')[1]
                posts = graph_api.request(request_path)
            else:
                posts = {}
