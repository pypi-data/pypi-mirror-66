# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import ItemType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from . import events
from . import mime_types


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'id',
            'description',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    event_types = events.DetailSerializer(
        many=True,
        read_only=True)
    mime_types = mime_types.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'id',
            'description',
            'mime_types',
            'icon',
            'event_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'description',
            'icon',
        )
