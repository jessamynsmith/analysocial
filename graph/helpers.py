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
                try:
                    graph_models.Post.objects.create(**post_data)
                except IntegrityError as e:
                    if not ignore_errors and str(e).find('duplicate key value') >= 0:
                        posts = {}
                        break

            if not retrieve_all or not posts:
                break

            next_page = posts.get('paging', {}).get('next')
            if next_page:
                posts = graph_api.request('me/posts?%s' % next_page.split('?')[1])
            else:
                posts = {}
