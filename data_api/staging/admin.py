from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from admin_extra_urls.extras import action, ExtraUrlMixin, link
from temba_client.v2 import TembaClient

from data_api.staging import models
from data_api.staging.models import Organization
from data_api.staging.tasks import import_org_with_client, sync_latest_data


class SyncCheckpointAdmin(admin.ModelAdmin):
    list_display = ['organization', 'collection_name', 'subcollection_name', 'last_started', 'last_saved',
                    'is_running']
    list_filter = ['is_running', 'organization', 'collection_name', 'last_started', 'last_saved']


class OrganizationAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ['name', 'country', 'is_active', 'server', 'api_token']
    list_filter = ['is_active', 'server']

    @link()
    def _sync_datawarehouse(self, request):
        sync_latest_data.delay()
        messages.add_message(request, messages.INFO, 'Task for Data Warehouse full sync has been scheduled')
        return HttpResponseRedirect(reverse('admin:staging_organization_changelist'))

    @action()
    def _sync_organization(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        client = TembaClient(organization.server, organization.api_token)
        import_org_with_client.delay(client, organization.server, organization.api_token)
        messages.add_message(request, messages.INFO, f'Task for importing {organization.name} has been scheduled')
        return HttpResponseRedirect(reverse('admin:staging_organization_change', args=[organization.pk]))

    @action()
    def _sync_latest_data(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        sync_latest_data.delay(entities=None, orgs=[organization.api_token])
        messages.add_message(request, messages.INFO, f'Task to sync data for {organization.name} has been scheduled')
        return HttpResponseRedirect(reverse('admin:staging_organization_change', args=[organization.pk]))


ORG_MODEL_FIELDS = ['organization', 'first_synced', 'last_synced']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS
    search_fields = ['name', 'uuid']


class FieldAdmin(admin.ModelAdmin):
    list_display = ['key', 'label', 'value_type'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid', 'country'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class ChannelEventAdmin(admin.ModelAdmin):
    list_display = ['type', 'contact', 'channel'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['text'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class LabelAdmin(admin.ModelAdmin):
    list_display = ['name'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class FlowAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class FlowStartAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'flow'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class CampaignEventAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'flow'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class MessageAdmin(admin.ModelAdmin):
    list_display = ['text', 'type', 'direction', 'sent_on', 'visibility'] + ORG_MODEL_FIELDS
    list_filter = ['type', 'direction', 'sent_on', 'visibility'] + ORG_MODEL_FIELDS


class RunAdmin(admin.ModelAdmin):
    list_display = ['flow', 'contact'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class BoundaryAdmin(admin.ModelAdmin):
    list_display = ['name'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class ResthookAdmin(admin.ModelAdmin):
    list_display = ['resthook'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class ResthookEventAdmin(admin.ModelAdmin):
    list_display = ['resthook', 'data'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


class ResthookSubscriberAdmin(admin.ModelAdmin):
    list_display = ['resthook', 'target_url'] + ORG_MODEL_FIELDS
    list_filter = ORG_MODEL_FIELDS


admin.site.register(models.SyncCheckpoint, SyncCheckpointAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.Channel, ChannelAdmin)
admin.site.register(models.ChannelEvent, ChannelEventAdmin)
admin.site.register(models.Broadcast, BroadcastAdmin)
admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Label, LabelAdmin)
admin.site.register(models.Flow, FlowAdmin)
admin.site.register(models.FlowStart, FlowStartAdmin)
admin.site.register(models.CampaignEvent, CampaignEventAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Run, RunAdmin)
admin.site.register(models.Boundary, BoundaryAdmin)
admin.site.register(models.Resthook, ResthookAdmin)
admin.site.register(models.ResthookEvent, ResthookEventAdmin)
admin.site.register(models.ResthookSubscriber, ResthookSubscriberAdmin)
