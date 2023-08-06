# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import MimeType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'url',
            'mime_type',
            'media_info_schema'
        )


class DescriptionSerializer(IrekuaModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'mime_type',
            'media_info_schema'
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'url',
            'mime_type',
            'media_info_schema',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'url',
            'mime_type',
            'media_info_schema',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'mime_type',
            'media_info_schema',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'mime_type',
            'media_info_schema',
        )
