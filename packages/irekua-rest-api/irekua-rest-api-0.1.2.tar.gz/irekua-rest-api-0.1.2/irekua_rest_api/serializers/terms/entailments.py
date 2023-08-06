# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Entailment

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from . import terms


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Entailment
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaHyperlinkedModelSerializer):
    source_type = serializers.CharField(
                read_only=True,
        source='source.term_type.name')
    source_value = serializers.CharField(
        read_only=True,
        source='source.value')
    target_type = serializers.CharField(
        read_only=True,
        source='target.term_type.name')
    target_value = serializers.CharField(
        read_only=True,
        source='target.value')


    class Meta:
        model = Entailment
        fields = (
            'url',
            'id',
            'source_type',
            'source_value',
            'target_type',
            'target_value',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    source = terms.ListSerializer(many=False, read_only=True)
    target = terms.ListSerializer(many=False, read_only=True)

    class Meta:
        model = Entailment
        fields = (
            'url',
            'id',
            'source',
            'target',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Entailment
        fields = (
            'source',
            'target',
            'metadata',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Entailment
        fields = (
            'metadata',
        )
