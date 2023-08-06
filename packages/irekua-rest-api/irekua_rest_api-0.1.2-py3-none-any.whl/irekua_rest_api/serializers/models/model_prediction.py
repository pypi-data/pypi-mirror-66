# -*- coding: utf-8 -*-
from irekua_models.models import ModelPrediction

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.models import model_version
from irekua_rest_api.serializers.items import items
from irekua_rest_api.serializers.object_types import events
from irekua_rest_api.serializers.terms import terms
from irekua_rest_api.serializers.users import users


class SelectSerializer(IrekuaModelSerializer):
    model_version = model_version.SelectSerializer(read_only=True)
    item = items.SelectSerializer(read_only=True)

    class Meta:
        model = ModelPrediction
        fields = ('url', 'id', 'item', 'model_version')


class ListSerializer(IrekuaModelSerializer):
    model_version = model_version.SelectSerializer(read_only=True)
    item = items.SelectSerializer(read_only=True)
    event_type = events.SelectSerializer(read_only=True)

    class Meta:
        model = ModelPrediction
        fields = (
            'url',
            'id',
            'item',
            'model_version',
            'event_type',
            'certainty'
        )


class DetailSerializer(IrekuaModelSerializer):
    model_version = model_version.ListSerializer(read_only=True)
    item = items.ListSerializer(read_only=True)
    event_type = events.ListSerializer(read_only=True)
    labels = terms.ListSerializer(read_only=True, many=True)
    created_by = users.SelectSerializer(read_only=True)
    modified_by = users.SelectSerializer(read_only=True)

    class Meta:
        model = ModelPrediction
        fields = (
            'url',
            'id',
            'item',
            'model_version',
            'event_type',
            'certainty',
            'labels',
            'annotation',
            'created_by',
            'modified_by',
            'created_on',
            'modified_on'
        )

        extra_kwargs = {
            'labels': {'style': {'base_template': 'input.html'}},
        }


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = ModelPrediction
        fields = (
            'item',
            'model_version',
            'event_type',
            'certainty',
            'labels',
            'annotation',
        )

        extra_kwargs = {
            'item': {'style': {'base_template': 'input.html'}},
            'labels': {'style': {'base_template': 'input.html'}},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = ModelPrediction
        fields = (
            'certainty',
            'labels',
            'annotation',
        )

        extra_kwargs = {
            'labels': {'style': {'base_template': 'input.html'}},
        }

    def update(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().create(validated_data)
