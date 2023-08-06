# -*- coding: utf-8 -*-
from irekua_models.models import ModelVersion

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.models import model


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = ModelVersion
        fields = ('url', 'id', 'model', 'version')


class ListSerializer(IrekuaModelSerializer):
    model = model.SelectSerializer(read_only=True)

    class Meta:
        model = ModelVersion
        fields = (
            'url',
            'id',
            'model',
            'version',
        )


class DetailSerializer(IrekuaModelSerializer):
    model = model.ListSerializer(read_only=True)

    class Meta:
        model = ModelVersion
        fields = (
            'url',
            'id',
            'model',
            'version',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = ModelVersion
        fields = ('model', 'version')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = ModelVersion
        fields = ('version',)

    def update(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().create(validated_data)
