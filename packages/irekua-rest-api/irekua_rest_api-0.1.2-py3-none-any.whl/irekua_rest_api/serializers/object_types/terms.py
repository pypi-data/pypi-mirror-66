# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import TermType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=TermType.objects.all())

    class Meta:
        model = TermType
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = TermType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = TermType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = TermType
        fields = (
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = TermType
        fields = (
            'description',
            'icon',
        )
