# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import Collection
from irekua_database.models import CollectionUser

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types.data_collections import types
from irekua_rest_api.serializers.users import institutions


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'url',
            'name',
            'logo',
            'collection_type',
            'description',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    collection_type = types.SelectSerializer(
        many=False,
        read_only=False)
    institution = institutions.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = Collection
        fields = (
            'url',
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'logo',
            'created_on',
            'modified_on',
        )


class UserData(IrekuaModelSerializer):
    class Meta:
        model = CollectionUser
        fields = (
            'role',
            'metadata'
        )


class CreateSerializer(IrekuaModelSerializer):
    user_data = UserData(many=False, read_only=False)

    class Meta:
        model = Collection
        fields = (
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'user_data',
        )

    def create(self, validated_data):
        user = self.context['request'].user

        user_data = validated_data.pop('user_data')
        collection = Collection.objects.create(**validated_data)  # pylint: disable=E1101

        user_data['user'] = user
        user_data['collection'] = collection
        CollectionUser.objects.create(**user_data)  # pylint: disable=E1101

        collection.add_administrator(user)

        # Strange loading condition requires this line to be called
        # in order to correctly return parsed data in HTTP response
        self.data

        return collection


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'description',
            'logo',
            'metadata',
            'institution',
        )
