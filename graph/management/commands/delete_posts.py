import datetime
from dateutil.relativedelta import relativedelta
import pytz

from django.core.management.base import BaseCommand, CommandError

from allauth.socialaccount.models import SocialAccount

from graph import models as graph_models


class Command(BaseCommand):
    help = "Email previous day's posts to users"

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            dest='user_email',
            help='Delete posts for a given user.',
            required=True
        )
        parser.add_argument(
            '--year',
            type=int,
            dest='year',
            help='Delete posts for a given year.',
            required=True
        )

    def handle(self, *args, **options):
        year = options.get('year')
        user_email = options.get('user_email')
        social_accounts = SocialAccount.objects.filter(provider="facebook",
                                                       user__userprofile__receive_emails=True)
        if user_email:
            social_accounts = social_accounts.filter(user__email=user_email)

        if year:
            start_timestamp = datetime.datetime(year=year, month=1,
                                                day=1, hour=0, minute=0, second=0,
                                                tzinfo=pytz.UTC)
            end_timestamp = start_timestamp + relativedelta(years=1)
        else:
            today = datetime.date.today()
            yesterday = today - relativedelta(days=1)
            start_timestamp = datetime.datetime(year=yesterday.year, month=yesterday.month,
                                                day=yesterday.day, hour=0, minute=0, second=0,
                                                tzinfo=pytz.UTC)
            end_timestamp = start_timestamp + relativedelta(days=1)

        for social_account in social_accounts:
            posts = graph_models.Post.objects.filter(
                user=social_account.user, created_time__gte=start_timestamp,
                created_time__lt=end_timestamp)
            message = ['\nAbout to delete {} posts for user {} in year {}\n\n'.format(
                posts.count(), user_email, year)]

            message.append(
                'Are you sure you want to do this?\n\n'
                "Type 'yes' to continue, or 'no' to cancel: "
            )
            if input(''.join(message)) != 'yes':
                raise CommandError("Deleting posts cancelled.")

            posts.delete()
