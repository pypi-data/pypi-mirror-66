# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import CollectionRole

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.users import roles
from . import types


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionRole
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionRole
        fields = (
            'url',
            'id',
            'role',
            'metadata_schema',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    role = roles.SelectSerializer(
        many=False,
        read_only=True)
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = CollectionRole
        fields = (
            'url',
            'id',
            'collection_type',
            'role',
            'metadata_schema',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionRole
        fields = (
            'role',
            'metadata_schema',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collection_type'] = collection_type
        return super().create(validated_data)
