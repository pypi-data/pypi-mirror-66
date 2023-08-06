# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import SamplingEventDevice

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.data_collections import devices
from irekua_rest_api.serializers import licences
from irekua_rest_api.serializers.users import users
from . import sampling_events


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventDevice
        fields = (
            'url',
            'id'
        )


class ListSerializer(IrekuaModelSerializer):
    device_type = serializers.CharField(
        read_only=True,
        source='collection_device.physical_device.device.device_type.name')
    device_internal_id = serializers.CharField(
        read_only=True,
        source='collection_device.internal_id')

    class Meta:
        model = SamplingEventDevice
        fields = (
            'url',
            'id',
            'sampling_event',
            'device_type',
            'device_internal_id',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    collection_device = devices.SelectSerializer(
        many=False,
        read_only=True)
    sampling_event = sampling_events.SelectSerializer(
        many=False,
        read_only=True)
    licence = licences.SelectSerializer(
        many=False,
        read_only=True)
    created_by = users.SelectSerializer(
        many=False,
        read_only=True)
    modified_by = users.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = SamplingEventDevice
        fields = (
            'url',
            'id',
            'sampling_event',
            'collection_device',
            'commentaries',
            'metadata',
            'configuration',
            'licence',
            'created_by',
            'created_on',
            'modified_on',
            'modified_by',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventDevice
        fields = (
            'collection_device',
            'commentaries',
            'metadata',
            'configuration',
            'licence',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            sampling_event = self.context['sampling_event']
            collection = sampling_event.collection

            collection_device = self.fields['collection_device']
            collection_device.queryset = collection.collectiondevice_set.all()

            licences_field = self.fields['licence']
            licences_field.queryset = collection.licence_set.all()

        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        sampling_event = self.context['sampling_event']
        user = self.context['request'].user

        validated_data['sampling_event'] = sampling_event
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventDevice
        fields = (
            'commentaries',
            'metadata',
            'configuration',
        )

    def update(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().create(validated_data)
