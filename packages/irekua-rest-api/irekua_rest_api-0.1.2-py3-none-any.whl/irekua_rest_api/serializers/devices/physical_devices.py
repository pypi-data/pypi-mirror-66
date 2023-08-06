# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import PhysicalDevice

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.users import users
from . import devices


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = PhysicalDevice
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    type = serializers.CharField(
        read_only=True,
        source='device.device_type.name')
    brand = serializers.CharField(
        read_only=True,
        source='device.brand.name')
    model = serializers.CharField(
        read_only=True,
        source='device.model')

    class Meta:
        model = PhysicalDevice
        fields = (
            'url',
            'id',
            'serial_number',
            'type',
            'brand',
            'model',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    device = devices.SelectSerializer(many=False, read_only=True)
    owner = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'owner',
            'metadata',
            'bundle',
            'device',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = PhysicalDevice
        fields = (
            'serial_number',
            'device',
            'metadata',
            'bundle',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = PhysicalDevice
        fields = (
            'serial_number',
            'metadata',
        )
