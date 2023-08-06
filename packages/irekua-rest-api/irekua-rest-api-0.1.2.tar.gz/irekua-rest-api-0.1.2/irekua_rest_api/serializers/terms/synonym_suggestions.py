# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import SynonymSuggestion

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.users import users
from . import terms


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = SynonymSuggestion
        fields = (
            'url',
            'id'
        )


class ListSerializer(IrekuaModelSerializer):
    source_type = serializers.CharField(
        read_only=True,
        source='source.term_type.name')
    source_value = serializers.CharField(
        read_only=True,
        source='source.value')

    class Meta:
        model = SynonymSuggestion
        fields = (
            'url',
            'source_type',
            'source_value',
            'synonym',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    source = terms.SelectSerializer(many=False, read_only=True)
    suggested_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = SynonymSuggestion
        fields = (
            'url',
            'id',
            'source',
            'synonym',
            'description',
            'metadata',
            'suggested_by',
            'suggested_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SynonymSuggestion
        fields = (
            'source',
            'synonym',
            'description',
            'metadata',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['suggested_by'] = user
        return super().create(validated_data)




class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = SynonymSuggestion
        fields = (
            'description',
            'metadata',
        )
