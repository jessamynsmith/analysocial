from django.core.management.base import BaseCommand

from graph import helpers


class Command(BaseCommand):
    help = 'Retrieve historical posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ignore-errors',
            action='store_true',
            dest='ignore-errors',
            default=False,
            help='Ignore any errors and continue retrieving posts.'
        )

    def handle(self, *args, **options):
        ignore_errors = options['ignore-errors']
        helpers.retrieve_facebook_posts(retrieve_all=True, ignore_errors=ignore_errors)
