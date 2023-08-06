# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionType
from irekua_database.models import AnnotationType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import annotations
from . import types


MODEL = CollectionType.annotation_types.through  # pylint: disable=E1101


class SelectSerializer(IrekuaModelSerializer):
    icon = serializers.URLField(source='annotationtype.icon.url')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'name',
            'icon',
        )


class ListSerializer(IrekuaModelSerializer):
    annotation_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='annotationtype')
    icon = serializers.ImageField(
        source='annotationtype.icon')
    annotation_schema = serializers.JSONField(
        source='annotationtype.annotation_schema')
    name = serializers.SlugRelatedField(
        read_only=True,
        source='annotationtype',
        slug_field='name')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'name',
            'annotation_type',
            'annotation_schema',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    annotation_type = annotations.SelectSerializer(
        many=False,
        read_only=True,
        source='annotationtype')
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'name',
            'collection_type',
            'annotation_type',
        )


class CreateSerializer(IrekuaModelSerializer):
    annotation_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=AnnotationType.objects.all(),  # pylint: disable=E1101
        source='annotationtype')

    class Meta:
        model = MODEL
        fields = (
            'annotation_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
