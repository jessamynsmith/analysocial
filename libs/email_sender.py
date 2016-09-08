from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.utils import formataddr


def send(recipient, subject, text_body, html_body, attachments=[]):
    recipients = [formataddr((recipient.get_full_name(), recipient.email))]
    msg = EmailMultiAlternatives(subject, text_body, to=recipients,
                                 reply_to=settings.REPLY_TO)
    for attachment in attachments:
        msg.attach(*attachment)
    if html_body:
        msg.attach_alternative(html_body, "text/html")
    msg.send()
    return True
