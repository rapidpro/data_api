from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^import_org/$', views.import_org_view),
    url(r'^import_status/$', views.import_status, name='import_status'),
    url(r'^import_status/mark_completed/(?P<last_saved_id>[\w]+)/$', views.mark_completed, name='mark_completed'),
)
