# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import SiteType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema'
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'name',
            'description',
            'metadata_schema'
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'description',
        )
