# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Annotation
from irekua_database.models import AnnotationTool

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.terms.terms import ListSerializer as TermListSerializer
from irekua_rest_api.serializers.terms.terms import ComplexTermSerializer
from irekua_rest_api.serializers.users.users import ListSerializer as UserListSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    labels = TermListSerializer(many=True)
    created_by = UserListSerializer()

    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
            'item',
            'event_type',
            'annotation',
            'annotation_type',
            'created_on',
            'created_by',
            'labels'
        )


class DetailSerializer(IrekuaModelSerializer):
    labels = ComplexTermSerializer(many=True)

    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
            'annotation_tool',
            'visualizer',
            'item',
            'event_type',
            'labels',
            'annotation_type',
            'annotation',
            'visualizer_configuration',
            'certainty',
            'quality',
            'commentaries',
            'created_on',
            'modified_on',
            'created_by',
            'modified_by',
        )


class AnnotationToolSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    version = serializers.CharField(required=True)
    logo = serializers.CharField(required=False)
    website = serializers.CharField(required=False)
    configuration_schema = serializers.JSONField(required=False)


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'event_type',
            'annotation',
            'labels',
            'certainty',
            'quality',
            'commentaries',
            'annotation_tool',
            'visualizer',
            'visualizer_configuration',
            'annotation_type',
        )

    def create(self, validated_data):
        item = self.context['item']
        user = self.context['request'].user

        validated_data['item'] = item
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'annotation',
            'labels',
            'certainty',
            'quality',
            'commentaries',
            'visualizer_configuration',
        )

    def update(self, instance, validated_data):
        user = self.context['request'].user

        validated_data['modified_by'] = user
        return super().update(instance, validated_data)
