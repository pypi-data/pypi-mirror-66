# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionType
from irekua_database.models import SamplingEventType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import sampling_events
from . import types


MODEL = CollectionType.sampling_event_types.through  # pylint: disable=E1101


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    sampling_event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'sampling_event_type',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    sampling_event_type = sampling_events.types.SelectSerializer(
        many=False,
        read_only=True,
        source='samplingeventtype')
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection_type',
            'sampling_event_type',
        )


class CreateSerializer(IrekuaModelSerializer):
    sampling_event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=SamplingEventType.objects.all(),  # pylint: disable=E1101
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'sampling_event_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
