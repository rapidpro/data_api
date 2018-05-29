from rest_framework import serializers

from data_api.staging.models import Group, Channel, Device, Contact, ChannelEvent, Field, Broadcast, Campaign


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
