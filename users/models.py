from allauth.socialaccount import signals as allauth_signals


def update_user_email(request, sociallogin, **kwargs):
    if not sociallogin.user.email:
        sociallogin.user.email = sociallogin.email_addresses[0].email
        sociallogin.user.save()


allauth_signals.pre_social_login.connect(update_user_email)

# TODO when new user signs up, add task to queue to retrieve all their posts
