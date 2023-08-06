# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import MetaCollection

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.users import users


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(IrekuaModelSerializer):
    created_by = users.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = MetaCollection
        fields = (
            'url',
            'name',
            'description',
            'created_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'name',
            'description',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'description',
        )
