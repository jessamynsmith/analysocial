from django.db import models
from django.template.defaultfilters import truncatewords
from django.conf import settings

from allauth.socialaccount import signals as allauth_signals


class Post(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    created_time = models.DateTimeField()
    story = models.TextField()
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        message = truncatewords(self.message, 10)
        return '%s: %s (%s - %s)' % (self.user, message, self.created_time, self.id)


def update_user_email(request, sociallogin, **kwargs):
    if not sociallogin.user.email:
        sociallogin.user.email = sociallogin.email_addresses[0].email
        sociallogin.user.save()


allauth_signals.pre_social_login.connect(update_user_email)
