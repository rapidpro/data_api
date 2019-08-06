import logging

from django.core.management import BaseCommand

from temba_client.v2 import TembaClient

from data_api.staging.models import logger as model_logger
from data_api.staging.tasks import import_org_with_client, logger as task_logger, sync_latest_data


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
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
            for logger in (task_logger, model_logger):
                logger.addHandler(console_handler)
                logger.setLevel(logging.INFO)
                print('set console logging. you should see another message following this one')
                logger.info('console logging is working!')

        client = TembaClient(server, api_key)
        import_org_with_client(client, server, api_key)
        sync_latest_data(orgs=[api_key])
