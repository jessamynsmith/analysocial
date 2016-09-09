from django.core.management.base import BaseCommand

from graph import helpers


class Command(BaseCommand):
    help = 'Retrieve historical posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--retrieve-all',
            action='store_true',
            dest='retrieve_all',
            default=False,
            help='Retrieve all posts.'
        )

        parser.add_argument(
            '--ignore-errors',
            action='store_true',
            dest='ignore_errors',
            default=False,
            help='Ignore any errors and continue retrieving posts.'
        )

    def handle(self, *args, **options):
        retrieve_all = options['retrieve_all']
        ignore_errors = options['ignore_errors']
        helpers.retrieve_facebook_posts(retrieve_all=retrieve_all, ignore_errors=ignore_errors)
