# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import EventType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from . import terms


class SelectSerializer(IrekuaModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=EventType.objects.all())

    class Meta:
        model = EventType
        fields = (
            'url',
            'name',
            'id',
        )


class DescriptionSerializer(IrekuaModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'name',
            'description',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'url',
            'id',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    term_types = terms.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = EventType
        fields = (
            'url',
            'id',
            'name',
            'description',
            'icon',
            'term_types',
            'created_on',
            'modified_on'
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'description',
            'icon',
        )
