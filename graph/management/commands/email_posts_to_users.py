import datetime
from dateutil.relativedelta import relativedelta
import pytz
from smtplib import SMTPDataError

from allauth.socialaccount.models import SocialAccount
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from graph import models as graph_models
from libs import email_sender


class Command(BaseCommand):
    help = "Email previous day's posts to users"

    def handle(self, *args, **options):
        social_accounts = SocialAccount.objects.all()

        for social_account in social_accounts:
            if social_account.provider.lower() != "facebook":
                continue

            today = datetime.date.today()
            yesterday = today - relativedelta(days=1)
            yesterday_start = datetime.datetime(year=yesterday.year, month=yesterday.month,
                                                day=yesterday.day, hour=0, minute=0, second=0,
                                                tzinfo=pytz.UTC)
            today_start = datetime.datetime(year=today.year, month=today.month,
                                                day=today.day, hour=0, minute=0, second=0,
                                                tzinfo=pytz.UTC)
            posts = graph_models.Post.objects.filter(user=social_account.user,
                                                     created_time__gte=yesterday_start,
                                                     created_time__lt=today_start)

            context = {
                'yesterday': yesterday,
                'num_posts': len(posts),
            }
            template_name = 'posts_notify'
            subject = "Yesterday's Facebook post summary"
            plaintext = get_template('graph/email/%s.txt' % template_name)
            html = get_template('graph/email/%s.html' % template_name)
            try:
                email_sender.send(social_account.user, subject, plaintext.render(context),
                                  html.render(context))
            except SMTPDataError as e:
                print(e)
