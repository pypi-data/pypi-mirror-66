# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import DeviceType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'url',
            'id',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'url',
            'id',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'url',
            'id',
            'name',
            'description',
            'icon',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'id',
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'description',
            'icon',
        )
