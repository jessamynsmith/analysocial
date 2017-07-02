from django.core.management.base import BaseCommand

from allauth.socialaccount.models import SocialAccount

from graph import helpers


class Command(BaseCommand):
    help = 'Retrieve historical messages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            dest='user_email',
            help='Get posts for a given user.'
        )

        parser.add_argument(
            '--retrieve-all',
            action='store_true',
            dest='retrieve_all',
            default=False,
            help='Retrieve all posts.'
        )

        parser.add_argument(
            '--ignore-errors',
            action='store_true',
            dest='ignore_errors',
            default=False,
            help='Ignore any errors and continue retrieving posts.'
        )

    def handle(self, *args, **options):
        retrieve_all = options['retrieve_all']
        ignore_errors = options['ignore_errors']

        user = None
        user_email = options.get('user_email')
        if user_email:
            social_account = SocialAccount.objects.get(user__email=user_email, provider="facebook")
            user = social_account.user

        helpers.retrieve_facebook_messages(user=user, retrieve_all=retrieve_all,
                                           ignore_errors=ignore_errors)
