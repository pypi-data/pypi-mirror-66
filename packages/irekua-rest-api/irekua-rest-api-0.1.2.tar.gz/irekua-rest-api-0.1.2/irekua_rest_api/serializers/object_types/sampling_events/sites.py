# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import SamplingEventType
from irekua_database.models import SiteType

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer
from irekua_rest_api.serializers.object_types import sites
from . import types


MODEL = SamplingEventType.site_types.through  # pylint: disable=E1101


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(IrekuaModelSerializer):
    site_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='sitetype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'site_type',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    site_type = sites.SelectSerializer(
        many=False,
        read_only=True,
        source='sitetype')
    sampling_event_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'site_type',
        )


class CreateSerializer(IrekuaModelSerializer):
    site_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=SiteType.objects.all(),  # pylint: disable=E1101
        source='sitetype')

    class Meta:
        model = MODEL
        fields = (
            'site_type',
        )

    def create(self, validated_data):
        sampling_event_type = self.context['sampling_event_type']
        validated_data['samplingeventtype'] = sampling_event_type
        return super().create(validated_data)
