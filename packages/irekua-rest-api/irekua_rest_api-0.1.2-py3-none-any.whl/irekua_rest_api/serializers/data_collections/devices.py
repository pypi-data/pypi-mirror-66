# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionDevice

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.devices import physical_devices


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionDevice
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    physical_device = serializers.StringRelatedField(
        many=False,
        read_only=True)

    class Meta:
        model = CollectionDevice
        fields = (
            'url',
            'id',
            'physical_device',
            'internal_id',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    physical_device = physical_devices.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = CollectionDevice
        fields = (
            'url',
            'physical_device',
            'internal_id',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionDevice
        fields = (
            'physical_device',
            'metadata',
            'internal_id',
        )

    def create(self, validated_data):
        collection = self.context['collection']
        validated_data['collection'] = collection
        return super().create(validated_data)
