import datetime
from dateutil.relativedelta import relativedelta
import pytz
from smtplib import SMTPDataError

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from allauth.socialaccount.models import SocialAccount

from graph import models as graph_models
from libs import email_sender, helpers


class Command(BaseCommand):
    help = "Email previous day's posts to users"

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            dest='user_email',
            help='Get posts for a given user.'
        )
        parser.add_argument(
            '--year',
            type=int,
            dest='year',
            help='Get posts for a given year.'
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
            posts_date = year
        else:
            today = datetime.date.today()
            yesterday = today - relativedelta(days=1)
            start_timestamp = datetime.datetime(year=yesterday.year, month=yesterday.month,
                                                day=yesterday.day, hour=0, minute=0, second=0,
                                                tzinfo=pytz.UTC)
            end_timestamp = start_timestamp + relativedelta(days=1)
            posts_date = start_timestamp.date()

        for social_account in social_accounts:
            data = {
                'posts': graph_models.Post.objects.filter(
                    user=social_account.user, created_time__gte=start_timestamp,
                    created_time__lt=end_timestamp).order_by('created_time').values(
                    'created_time', 'story', 'message', 'attachment__url', 'attachment__title',
                    'attachment__type', 'attachment__description'
                ),
            }
            post_ids = data['posts'].values_list('id')
            data['comments'] = graph_models.Comment.objects.filter(
                post__in=post_ids).order_by('post__id').values()

            context = {
                'full_name': social_account.user.get_full_name(),
                'posts_date': posts_date,
                'num_posts': len(data['posts']),
                'admin_name': settings.ADMINS[0][0],
                'full_domain': helpers.get_full_domain(),
            }
            template_name = 'posts_notify'
            subject = "%s Facebook post summary" % posts_date
            plaintext = get_template('graph/email/%s.txt' % template_name)
            html = get_template('graph/email/%s.html' % template_name)

            email_attachments = []
            for data_type in data:
                csvfile = helpers.create_csv(data[data_type])
                csv_data = csvfile.getvalue().decode('utf-8')
                email_attachments.append(['facebook_%s_%s.csv' % (data_type, posts_date), csv_data,
                                         'text/csv'])
            try:
                email_sender.send(social_account.user, subject, plaintext.render(context),
                                  html.render(context), email_attachments)
            except SMTPDataError as e:
                print(e)
