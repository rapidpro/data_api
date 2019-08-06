import logging
from datetime import datetime

from django.conf import settings
from django.core.mail import mail_admins

from celery import task
from retrying import retry
from sentry_sdk import capture_exception
from temba_client.exceptions import TembaBadRequestError, TembaConnectionError, TembaRateExceededError, TembaTokenError

from data_api.staging.models import Organization

logging.basicConfig(format=settings.LOG_FORMAT)
logger = logging.getLogger("tasks")


def retry_if_temba_api_or_connection_error(exception):
    if isinstance(exception, (TembaBadRequestError, TembaTokenError)):
        return False
    if isinstance(exception, (TembaConnectionError, TembaRateExceededError)):
        logger.warning("Raised an exception: %s - Retrying in %s minutes", str(exception),
                       str(settings.RETRY_WAIT_FIXED / 60000))
        return True
    return False


@retry(retry_on_exception=retry_if_temba_api_or_connection_error, stop_max_attempt_number=settings.RETRY_MAX_ATTEMPTS,
       wait_fixed=settings.RETRY_WAIT_FIXED)
def fetch_entity(entity, org, return_objs=False):
    logger.info("Fetching objects of type: %s for Org: %s", str(entity), org.name)
    return entity.sync_all_data(org, return_objs)


@task
def import_org_with_client(client, server, api_key):
    org = client.get_org()
    org_dict = org.serialize()
    org_dict['api_token'] = api_key
    org_dict['server'] = server
    org_dict['is_active'] = True
    try:
        local_org = Organization.objects.get(api_token=api_key)
        for k, v in org_dict.items():
            setattr(local_org, k, v)
        local_org.save()
        return local_org
    except Organization.DoesNotExist:
        return Organization.objects.create(**org_dict)


@task
def sync_latest_data(entities=None, orgs=None):
    """
    Syncs the latest data from configured rapidpro Orgs.

    The default value for both arguments is to sync _all_ entities/orgs.
    """
    mail_admins('Starting RapidPro data sync', '')
    start_time = datetime.now()
    if not entities:
        entities = _get_org_entities()
    if not orgs:
        orgs = _get_all_orgs()
    else:
        orgs = _get_orgs_by_api_keys(orgs)
    assert iter(entities)
    for org in orgs:
        for entity in entities:
            try:
                fetch_entity(entity, org)
            except Exception as e:
                if settings.DEBUG:
                    raise
                capture_exception(e)

    task_duration = datetime.now() - start_time
    mail_admins('Finished RapidPro data sync in {} seconds'.format(task_duration.seconds), '')


def _get_org_entities():
    import data_api.staging.models as staging_models
    return [
        staging_models.Group,
        staging_models.Contact,
        staging_models.Field,
        staging_models.Channel,
        staging_models.ChannelEvent,
        staging_models.Broadcast,
        staging_models.Campaign,
        staging_models.Label,
        staging_models.Flow,
        staging_models.FlowStart,
        staging_models.CampaignEvent,
        staging_models.Message,
        staging_models.Run,
        staging_models.Boundary,
        staging_models.Resthook,
        staging_models.ResthookEvent,
        staging_models.ResthookSubscriber,
    ]


def _get_all_orgs():
    from data_api.staging.models import Organization
    return Organization.objects.filter(is_active=True)


def _get_orgs_by_api_keys(api_keys):
    from data_api.staging.models import Organization
    return Organization.objects.filter(api_token__in=api_keys)
