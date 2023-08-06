# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import SamplingEventType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name'
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name',
            'icon',
            'description',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'description',
            'icon',
        )
