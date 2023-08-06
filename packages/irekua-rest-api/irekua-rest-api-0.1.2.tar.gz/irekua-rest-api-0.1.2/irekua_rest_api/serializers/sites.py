# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from irekua_database.models import Site
from irekua_database.models import SamplingEvent
from irekua_database.models import SamplingEventDevice
from irekua_database.models import CollectionSite
from irekua_database.models import Item

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.users import users


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Site
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    created_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'created_by',
            'created_on',
            'modified_on',
        )


class FullDetailSerializer(IrekuaHyperlinkedModelSerializer):
    created_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'latitude',
            'longitude',
            'geo_ref',
            'altitude',
            'created_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
            'latitude',
            'longitude',
            'altitude',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
            'altitude',
        )


class GeometrySerializer(IrekuaModelSerializer):
    class Meta:
        model = Site
        fields = (
            'latitude',
            'longitude',
            'altitude',
            'geo_ref',
        )


class SiteLocationSerializer(IrekuaModelSerializer):
    geometry = GeometrySerializer(read_only=True, source="*")

    class Meta:
        model = Site
        fields = (
            'id',
            'geometry'
        )

class SamplingEventLocationSerializer(IrekuaModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="collection_site.site")

    class Meta:
        model = SamplingEvent
        fields = (
            'id',
            'geometry'
        )

class SamplingEventDeviceLocationSerializer(IrekuaModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="sampling_event.collection_site.site")

    class Meta:
        model = SamplingEventDevice
        fields = (
            'id',
            'geometry'
        )


class ItemLocationSerializer(IrekuaModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="sampling_event_device.sampling_event.collection_site.site")

    class Meta:
        model = Item
        fields = (
            'id',
            'geometry'
        )

class CollectionSiteLocationSerializer(IrekuaModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="site")

    class Meta:
        model = CollectionSite
        fields = (
            'id',
            'geometry'
        )
