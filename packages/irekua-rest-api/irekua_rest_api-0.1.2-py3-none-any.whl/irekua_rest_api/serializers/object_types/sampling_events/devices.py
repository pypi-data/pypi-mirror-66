# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import SamplingEventTypeDeviceType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import devices
from . import types


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'url',
            'id'
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'device_type',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    device_type = devices.SelectSerializer(
        many=False,
        read_only=True)
    sampling_event_type = types.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'device_type',
            'metadata_schema',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'device_type',
            'metadata_schema',
        )

    def create(self, validated_data):
        sampling_event_type = self.context['sampling_event_type']
        validated_data['sampling_event_type'] = sampling_event_type
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'metadata_schema',
        )
