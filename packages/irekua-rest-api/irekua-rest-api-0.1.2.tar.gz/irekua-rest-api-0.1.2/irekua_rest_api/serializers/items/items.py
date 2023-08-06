# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Item

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import items
from irekua_rest_api.serializers.object_types import events
from irekua_rest_api.serializers.sampling_events import devices
from irekua_rest_api.serializers import licences
from . import tags


class SelectSerializer(IrekuaModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=Item.objects.all())  # pylint: disable=E1101

    class Meta:
        model = Item
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Item
        fields = (
            'url',
            'id',
            'item_type',
            'captured_on',
        )


class ListCollectionSerializer(IrekuaModelSerializer):
    collection = serializers.CharField(
        source='sampling_event_device.sampling_event.collection',
        read_only=True,
        label="collection")

    class Meta:
        model = Item
        fields = (
            'url',
            'id',
            'item_type',
            'captured_on',
        )


class DetailSerializer(IrekuaModelSerializer):
    item_type = items.SelectSerializer(many=False, read_only=True)
    sampling_event_device = devices.SelectSerializer(many=False, read_only=True)
    licence = licences.SelectSerializer(many=False, read_only=True)
    tags = tags.SelectSerializer(many=True, read_only=True)
    ready_event_types = events.SelectSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = (
            'url',
            'id',
            'hash',
            'item_type',
            'media_info',
            'metadata',
            'sampling_event_device',
            'captured_on',
            'licence',
            'tags',
            'ready_event_types',
            'created_on',
            'modified_on',
            'created_by',
            'modified_by',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Item
        fields = (
            'hash',
            'item_file',
            'item_type',
            'media_info',
            'metadata',
            'captured_on',
            'licence',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        licence_field = self.fields['licence']
        item_type_field = self.fields['item_type']

        try:
            sampling_event_device = self.context['sampling_event_device']

            collection = sampling_event_device.sampling_event.collection
            licence_field.queryset = collection.licence_set.all()

            collection_type = collection.collection_type
            if collection_type.restrict_item_types:
                item_type_field.queryset = (
                    collection_type.item_types.all()
                )

        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        user = self.context['request'].user
        sampling_event_device = self.context['sampling_event_device']

        validated_data['sampling_event_device'] = sampling_event_device
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Item
        fields = (
            'metadata',
        )


    def update(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().update(validated_data)


class DownloadSerializer(IrekuaModelSerializer):
    class Meta:
        model = Item
        fields = (
            'item_file',
        )
