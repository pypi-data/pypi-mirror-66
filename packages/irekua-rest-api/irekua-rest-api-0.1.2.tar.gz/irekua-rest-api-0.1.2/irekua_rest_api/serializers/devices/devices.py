# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import Device

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import devices
from . import brands


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Device
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Device
        fields = (
            'url',
            'id',
            'device_type',
            'brand',
            'model',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    device_type = devices.SelectSerializer(
        many=False,
        read_only=True)
    brand = brands.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = Device
        fields = (
            'url',
            'id',
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Device
        fields = (
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
        )
