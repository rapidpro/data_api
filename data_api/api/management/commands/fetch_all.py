import logging
from django.core.management import BaseCommand
from data_api.api.tasks import sync_latest_data, logger
from data_api.api.utils import import_org


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('api_key')

        # Named (optional) arguments
        parser.add_argument(
            '--server',
            action='store',
            dest='server',
            default='https://app.rapidpro.io',
            help='Bootstrap an org from an API key',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='log_to_console',
            default=False,
            help='Log all output to console.',
        )

    def handle(self, api_key, server, *args, **options):
        if options['log_to_console']:
            # create console handler with a higher log level
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            logger.addHandler(console_handler)
            logger.setLevel(logging.DEBUG)
            print('set console logging. you should see another message following this one')
            logger.debug('console logging is working!')

        import_org(server, api_key)
        sync_latest_data(orgs=[api_key])
