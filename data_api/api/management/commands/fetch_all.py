from django.core.management import BaseCommand
from data_api.api.tasks import sync_latest_data
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

    def handle(self, api_key, server, *args, **options):
        import_org(server, api_key)
        sync_latest_data(orgs=[api_key])