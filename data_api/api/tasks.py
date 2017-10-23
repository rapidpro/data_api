import logging
import traceback
from django.conf import settings
import requests
from retrying import retry
from temba_client.exceptions import TembaConnectionError, TembaBadRequestError, TembaTokenError, \
    TembaRateExceededError, TembaException
from data_api.api.models import BaseUtil, Org, Message, Run
from djcelery_transactions import task

__author__ = 'kenneth'

logging.basicConfig(format=settings.LOG_FORMAT)
logger = logging.getLogger("tasks")


def retry_if_temba_api_or_connection_error(exception):
    if isinstance(exception, (TembaBadRequestError, TembaTokenError)):
        return False
    if isinstance(exception, (TembaConnectionError, TembaRateExceededError)):
        logger.warning("Raised an exception: %s - Retrying in %s minutes", str(exception),
                       str(settings.RETRY_WAIT_FIXED/60000))
        return True
    return False


@retry(retry_on_exception=retry_if_temba_api_or_connection_error, stop_max_attempt_number=settings.RETRY_MAX_ATTEMPTS,
       wait_fixed=settings.RETRY_WAIT_FIXED)
def fetch_entity(entity, org):
    logger.info("Fetching Object of type: %s for Org: %s", str(entity), org.name)
    entity.fetch_objects(org)


@task
def fetch_all(entities=None, orgs=None):
    if not entities:
        entities = BaseUtil.__subclasses__()
    if not orgs:
        orgs = Org.objects.filter(is_active=True)
    else:
        orgs = [Org.objects.get(**{'api_token': api_key}) for api_key in orgs]
    assert iter(entities)
    for org in orgs:
        for entity in entities:
            try:
                fetch_entity(entity, org)
            except TembaException as e:
                if settings.DEBUG:
                    raise
                logger.error("Temba is misbehaving: %s - No retry", str(e))
                continue
            except Exception as e:
                if settings.DEBUG:
                    raise
                logger.error("Things are dead: %s - No retry", str(traceback.format_exc()))


@task
def generate_message_dumps(from_date=None, org=None, contact_fields=None):
    Message.generate_csv(from_date=from_date, org_id=org, contact_fields=contact_fields)

@task
def generate_run_dumps(from_date=None, org=None, contact_fields=None):
    Run.generate_csv(from_date=from_date, org_id=org, contact_fields=contact_fields)
