from rest_framework_mongoengine import serializers
from data_api.api.models import Run, Flow, Contact, FlowStep, RunValueSet

__author__ = 'kenneth'


class FlowStepReadSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = FlowStep
        exclude = ('text',)


class RunValueSetReadSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = RunValueSet
        exclude = ('text',)


class ContactReadSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'uuid', 'groups', 'fields', 'language')


class RunReadSerializer(serializers.DocumentSerializer):
    contact = ContactReadSerializer()
    values = RunValueSetReadSerializer(many=True)
    steps = FlowStepReadSerializer(many=True)

    class Meta:
        model = Run
        depth = 3
        exclude = ('tid', 'modified_on')

    def update(self, instance, validated_data):
        values = validated_data.pop('values')
        steps = validated_data.pop('steps')
        updated_instance = super(RunReadSerializer, self).update(instance, validated_data)

        for value_data in values:
            updated_instance.values.append(RunValueSet(**value_data))

        for step_data in steps:
            updated_instance.steps.append(FlowStep(**step_data))

        updated_instance.save()
        return updated_instance


class FlowReadSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Flow
        depth = 3
