from rest_framework import serializers
from being.models import Being
from feed_events.models import BeingsEvent, BeingsListEvent


class BeingListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Being

        fields = [
            'id',
            'name',
            'state',
            'url',
        ]
        read_only_fields = [
            'state',
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class BeingDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Being
        fields = [
            'id',
            'name',
            'state',
            'url',
        ]
        read_only_fields = [
            'name',
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class BeingEventSerializer(serializers.ModelSerializer):
    being_name = serializers.CharField(source='being.name')
    state = serializers.CharField(source='being.state')

    class Meta:
        model = BeingsEvent
        fields = [
            'being_name',
            'state',
            'prev_state',
        ]


class BeingsListEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = BeingsListEvent
        fields = [
            'get_event'
        ]