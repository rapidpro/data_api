from __future__ import absolute_import, unicode_literals
import os
import traceback
from celery import Celery
import sys

__author__ = 'kenneth'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_api.settings')

app = Celery('data_api')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        from data_api.api.tasks import sync_latest_data
    except Exception:
        # fail hard if something went wrong bootsrapping the tasks
        traceback.print_exc()
        sys.exit()

    seconds_in_a_week = 60*60*24*7
    update_interval = int(os.environ.get('FETCH_INTERVAL', seconds_in_a_week))
    sender.add_periodic_task(update_interval, sync_latest_data.s(),
                             name='Sync data from RapidPRO every {} seconds'.format(update_interval))

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
