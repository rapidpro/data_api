from django.core.management import BaseCommand

from temba_client.v2 import TembaClient

from data_api.staging.tasks import import_org_with_client


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('api_key')

        # Named (optional) arguments
        parser.add_argument(
            '--server',
            action='store',
            dest='server',
            default='https://app.rapidpro.io',
            help='Bootstrap an org from an API key',
        )

    def handle(self, api_key, server, *args, **options):
        print('server: {}, api key: {}'.format(server, api_key))
        client = TembaClient(server, api_key)
        import_org_with_client(client, server, api_key)
