from dateutil.relativedelta import relativedelta
from smtplib import SMTPDataError

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils import timezone

from allauth.socialaccount.models import SocialAccount

from libs import email_sender, helpers


class Command(BaseCommand):
    help = "Remind users to log in so their access tokens don't expire"

    def handle(self, *args, **options):
        now = timezone.now()
        last_month = now - relativedelta(days=30)

        social_accounts = SocialAccount.objects.filter(provider="facebook",
                                                       last_login__lte=last_month)

        for social_account in social_accounts:
            context = {
                'full_name': social_account.user.get_full_name(),
                'admin_name': settings.ADMINS[0][0],
                'full_domain': helpers.get_full_domain(),
            }
            template_name = 'login_reminder'
            subject = "Refresh Your Analysocial Facebook Login"
            plaintext = get_template('graph/email/%s.txt' % template_name)
            html = get_template('graph/email/%s.html' % template_name)

            try:
                email_sender.send(social_account.user, subject, plaintext.render(context),
                                  html.render(context))
            except SMTPDataError as e:
                print(e)
