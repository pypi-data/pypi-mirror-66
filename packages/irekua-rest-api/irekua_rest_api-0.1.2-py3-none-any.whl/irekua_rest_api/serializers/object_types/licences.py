# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import LicenceType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'description',
            'icon',
        )
