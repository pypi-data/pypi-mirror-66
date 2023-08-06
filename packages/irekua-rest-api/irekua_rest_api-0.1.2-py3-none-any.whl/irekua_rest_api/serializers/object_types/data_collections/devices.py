# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import CollectionDeviceType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import devices
from . import types


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionDeviceType
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionDeviceType
        fields = (
            'url',
            'id',
            'device_type',
            'metadata_schema',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    device_type = devices.SelectSerializer(
        many=False,
        read_only=True)
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = CollectionDeviceType
        fields = (
            'url',
            'id',
            'collection_type',
            'device_type',
            'metadata_schema',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionDeviceType
        fields = (
            'device_type',
            'metadata_schema',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collection_type'] = collection_type
        return super().create(validated_data)
