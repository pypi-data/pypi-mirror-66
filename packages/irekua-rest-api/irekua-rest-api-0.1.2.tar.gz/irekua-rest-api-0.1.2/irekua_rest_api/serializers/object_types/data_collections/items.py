# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionItemType

from irekua_rest_api.serializers.object_types import items

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import events
from irekua_rest_api.serializers.object_types import mime_types
from . import types


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    event_types = events.SelectSerializer(
        many=True,
        read_only=True,
        source='item_type.event_types')
    mime_types = mime_types.SelectSerializer(
        many=True,
        read_only=True,
        source='item_type.mime_types')
    name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        source='item_type')

    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'id',
            'name',
            'item_type',
            'event_types',
            'mime_types',
            'metadata_schema',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    item_type = items.SelectSerializer(
        many=False,
        read_only=True)
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True)
    event_types = events.SelectSerializer(
        many=True,
        read_only=True,
        source='item_type.event_types')
    mime_types = mime_types.SelectSerializer(
        many=True,
        read_only=True,
        source='item_type.mime_types')

    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'id',
            'collection_type',
            'item_type',
            'metadata_schema',
            'event_types',
            'mime_types',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionItemType
        fields = (
            'item_type',
            'metadata_schema',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collection_type'] = collection_type
        return super().create(validated_data)


class SimpleListSerializer(IrekuaModelSerializer):
    event_types = events.DescriptionSerializer(
        many=True,
        read_only=True,
        source='item_type.event_types')
    mime_types = mime_types.DescriptionSerializer(
        many=True,
        read_only=True,
        source='item_type.mime_types')


    class Meta:
        model = CollectionItemType
        fields = (
            'id',
            'item_type',
            'event_types',
            'mime_types',
            'metadata_schema',
        )
