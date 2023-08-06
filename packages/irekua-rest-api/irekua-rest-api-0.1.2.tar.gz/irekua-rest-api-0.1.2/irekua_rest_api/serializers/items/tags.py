# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import Tag

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'url',
            'name',
            'description',
            'icon'
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'created_on',
            'modified_on'
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
            'description',
            'icon'
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'description',
            'icon'
        )
