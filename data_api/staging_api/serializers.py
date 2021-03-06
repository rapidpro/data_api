from rest_framework import serializers

from data_api.staging.models import (
    Boundary,
    Broadcast,
    Campaign,
    CampaignEvent,
    Channel,
    ChannelEvent,
    Contact,
    Device,
    Field,
    Flow,
    FlowStart,
    Group,
    Label,
    Resthook,
    ResthookEvent,
    ResthookSubscriber,
    Run,
)


def RapidproIdField():
    return serializers.IntegerField(source='rapidpro_id')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = '__all__'


class ChannelEventSerializer(serializers.ModelSerializer):
    id = RapidproIdField()

    class Meta:
        model = ChannelEvent
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = '__all__'


class BroadcastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Broadcast
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignEvent
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = '__all__'


class FlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flow
        fields = '__all__'


class FlowStartSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlowStart
        fields = '__all__'


class RunSerializer(serializers.ModelSerializer):
    id = RapidproIdField()

    class Meta:
        model = Run
        fields = '__all__'


class BoundarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Boundary
        fields = '__all__'


class ResthookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resthook
        fields = '__all__'


class ResthookEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResthookEvent
        fields = '__all__'


class ResthookSubscriberSerializer(serializers.ModelSerializer):
    id = RapidproIdField()

    class Meta:
        model = ResthookSubscriber
        fields = '__all__'
