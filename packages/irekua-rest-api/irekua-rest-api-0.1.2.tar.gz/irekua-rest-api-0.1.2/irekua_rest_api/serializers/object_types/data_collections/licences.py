# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionType
from irekua_database.models import LicenceType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import licences
from . import types


MODEL = CollectionType.licence_types.through  # pylint: disable=E1101


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    licence_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='licencetype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'licence_type',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    licence_type = licences.SelectSerializer(
        many=False,
        read_only=True,
        source='licencetype')
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection_type',
            'licence_type',
        )


class CreateSerializer(IrekuaModelSerializer):
    licence_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=LicenceType.objects.all(),  # pylint: disable=E1101
        source='licencetype')

    class Meta:
        model = MODEL
        fields = (
            'licence_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
