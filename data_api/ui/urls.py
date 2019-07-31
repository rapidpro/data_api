from django.conf.urls import url

from data_api.ui.views import import_org_view, SyncLastestData

urlpatterns = (
    url(r'^import_org/$', import_org_view),
    url(r'^tasks/sync_latest_data/$', SyncLastestData.as_view(), name='tasks_sync_latest_data'),
)
