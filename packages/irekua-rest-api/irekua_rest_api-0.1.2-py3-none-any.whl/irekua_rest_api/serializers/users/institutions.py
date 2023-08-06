# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import Institution

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'url',
            'id',
            'institution_name',
            'institution_code',
            'subdependency',
            'logo',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'url',
            'id',
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
        )
