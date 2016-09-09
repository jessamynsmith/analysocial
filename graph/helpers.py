import sys
import traceback

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
        request_path = 'me/posts/'
        posts = graph_api.request(request_path)

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
