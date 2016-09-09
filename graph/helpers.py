import facebook
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db import IntegrityError

from graph import models as graph_models


def retrieve_facebook_posts(user=None, retrieve_all=False, ignore_errors=False):
    social_accounts = SocialAccount.objects.all()
    if user:
        social_accounts = social_accounts.filter(user=user)

    for social_account in social_accounts:
        if social_account.provider.lower() != "facebook":
            continue

        access_token = social_account.socialtoken_set.all()[0].token
        version = settings.FACEBOOK_API_VERSION
        graph_api = facebook.GraphAPI(access_token=access_token, version=version)
        posts = graph_api.request('me/posts/')

        while 'data' in posts:
            for post_data in posts['data']:
                post_data['user'] = social_account.user
                post = graph_models.Post(**post_data)
                try:
                    post.save()
                except IntegrityError as e:
                    if str(e).find('duplicate key value') >= 0:
                        if not ignore_errors:
                            posts = {}
                            break
                    else:
                        raise e
                except Exception as e:
                    print(post_data)
                    raise e

                attachments = graph_api.request('%s/attachments/' % post_data['id'])
                for attachment_data in attachments['data']:
                    attachment_data['post'] = post
                    try:
                        attachment = graph_models.Attachment(**attachment_data)
                        attachment.save()
                    except IntegrityError as e:
                        if not str(e).find('duplicate key value') >= 0:
                            raise e
                    except Exception as e:
                        print(attachment_data)
                        raise e

                comments = graph_api.request('%s/comments/' % post_data['id'])
                for comment_data in comments['data']:
                    comment_data['post'] = post
                    comment_data['from_json'] = comment_data.pop('from')
                    try:
                        comment = graph_models.Comment(**comment_data)
                        comment.save()
                    except IntegrityError as e:
                        if not str(e).find('duplicate key value') >= 0:
                            raise e
                    except Exception as e:
                        print(comment_data)
                        raise e

            if not retrieve_all or not posts:
                break

            next_page = posts.get('paging', {}).get('next')
            if next_page:
                posts = graph_api.request('me/posts?%s' % next_page.split('?')[1])
            else:
                posts = {}
