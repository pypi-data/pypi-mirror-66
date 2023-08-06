# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import DeviceBrand

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'url',
            'name',
            'logo',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'url',
            'name',
            'website',
            'logo',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'name',
            'website',
            'logo',
        )
