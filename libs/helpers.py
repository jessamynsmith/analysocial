from io import BytesIO
import unicodecsv as csv

from django.conf import settings
from django.contrib.sites.models import Site


def get_full_domain():
    scheme = 'https'
    if not settings.SECURE_SSL_REDIRECT:
        scheme = 'http'
    return '%s://%s' % (scheme, Site.objects.get_current().domain)


def create_csv(values_queryset):
    output = BytesIO()
    writer = csv.writer(output, encoding='utf-8')
    if values_queryset.count() > 0:
        writer.writerow(values_queryset[0].keys())
    for item in values_queryset:
        writer.writerow(item.values())
    return output
