# -*- coding: utf-8 -*-
from irekua_models.models import Model

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.object_types import annotations
from irekua_rest_api.serializers.terms import terms


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Model
        fields = ('url', 'id', 'name')


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Model
        fields = (
            'url',
            'id',
            'name',
            'description'
        )


class DetailSerializer(IrekuaModelSerializer):
    annotation_type = annotations.SelectSerializer(read_only=True)
    terms = terms.ListSerializer(read_only=True, many=True)

    class Meta:
        model = Model
        fields = (
            'url',
            'id',
            'name',
            'description',
            'repository',
            'annotation_type',
            'terms',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Model
        fields = (
            'name',
            'description',
            'repository',
            'annotation_type',
            'terms',
            'event_types',
            'item_types',
        )

        extra_kwargs = {
            'terms': {'style': {'base_template': 'input.html'}},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Model
        fields = (
            'name',
            'description',
            'repository',
            'annotation_type',
            'terms',
            'event_types',
            'item_types',
        )

        extra_kwargs = {
            'terms': {'style': {'base_template': 'input.html'}},
        }

    def update(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().create(validated_data)
