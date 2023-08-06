# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import EntailmentType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import terms


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = EntailmentType


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = EntailmentType
        fields = (
            'url',
            'id',
            'source_type',
            'target_type',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    source_type = terms.SelectSerializer(many=False, read_only=True)
    target_type = terms.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = EntailmentType
        fields = (
            'url',
            'id',
            'source_type',
            'target_type',
            'metadata_schema',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = EntailmentType
        fields = (
            'source_type',
            'target_type',
            'metadata_schema',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = EntailmentType
        fields = (
            'metadata_schema',
        )
