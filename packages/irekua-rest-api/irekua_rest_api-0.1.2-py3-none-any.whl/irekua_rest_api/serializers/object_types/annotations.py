# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import AnnotationType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'url',
            'id',
            'name',
            'icon',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'url',
            'id',
            'name',
            'description',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'url',
            'id',
            'name',
            'description',
            'annotation_schema',
            'icon',
            'created_on',
            'modified_on'
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'name',
            'description',
            'annotation_schema',
            'icon',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'description',
            'icon',
        )
