# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import AnnotationVote
from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.users import users
from . import annotations


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = AnnotationVote
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = AnnotationVote
        fields = (
            'url',
            'id',
            'label',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    annotation = annotations.SelectSerializer(
        many=False,
        read_only=True)
    created_by = users.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = AnnotationVote
        fields = (
            'url',
            'id',
            'annotation',
            'label',
            'created_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    label = serializers.JSONField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            annotation = self.context['annotation']
            previous_label = annotation.label

            self.fields['label'].initial = previous_label
        except (KeyError, AttributeError):
            pass

    class Meta:
        model = AnnotationVote
        fields = (
            'label',
        )

    def create(self, validated_data):
        annotation = self.context['annotation']
        user = self.context['request'].user

        validated_data['annotation'] = annotation
        validated_data['created_by'] = user
        return super().create(validated_data)
