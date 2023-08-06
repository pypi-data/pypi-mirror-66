# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import CollectionType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
            'logo',
            'description',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'name',
            'logo',
            'description',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'logo',
            'description',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
            'description',
            'logo',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
            'created_on',
            'modified_on',
        )
