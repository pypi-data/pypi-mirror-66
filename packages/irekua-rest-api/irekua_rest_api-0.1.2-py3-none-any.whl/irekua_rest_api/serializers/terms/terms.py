# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Term

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import terms


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Term
        fields = (
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    term_type = terms.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Term
        fields = (
            'id',
            'term_type',
            'value',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    term_type = terms.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Term
        fields = (
            'id',
            'term_type',
            'value',
            'description',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Term
        fields = (
            'value',
            'description',
            'metadata'
        )

    def create(self, validated_data):
        validated_data['term_type'] = self.context['term_type']
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Term
        fields = (
            'description',
            'metadata'
        )


class EntailmentSerializer(serializers.Serializer):
    term_type = serializers.CharField(
        source='target.term_type')
    description = serializers.CharField(
        source='target.description')
    value = serializers.CharField(
        source='target.value')
    id = serializers.IntegerField(
        source='target.id')
    scope = serializers.CharField(
        source='target.scope')


class TermSerializer(IrekuaModelSerializer):
    term_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = Term
        fields = [
            'id',
            'scope',
            'term_type',
            'value',
            'description',
        ]


class ComplexTermSerializer(IrekuaModelSerializer):
    term_type = serializers.StringRelatedField(many=False)
    entailments = EntailmentSerializer(
        many=True,
        read_only=True,
        source='entailment_source')

    class Meta:
        model = Term
        fields = [
            'id',
            'scope',
            'term_type',
            'value',
            'description',
            'entailments',
        ]
