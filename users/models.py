from django.contrib.auth.models import User
from django.db import models

from allauth.socialaccount import signals as allauth_signals


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_emails = models.BooleanField(default=True)


def create_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'userprofile'):
        UserProfile(user=instance).save()


def update_user_email(request, sociallogin, **kwargs):
    if not sociallogin.user.email:
        sociallogin.user.email = sociallogin.email_addresses[0].email
        sociallogin.user.save()


models.signals.post_save.connect(create_user_profile, sender=User)
allauth_signals.pre_social_login.connect(update_user_email)

# TODO when new user signs up, add task to queue to retrieve all their posts
