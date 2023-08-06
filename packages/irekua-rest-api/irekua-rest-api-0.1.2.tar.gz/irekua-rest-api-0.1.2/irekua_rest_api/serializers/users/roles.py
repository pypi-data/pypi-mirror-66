# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from rest_framework import serializers

from irekua_database.models import Role

from irekua_rest_api.serializers.base import IrekuaModelSerializer
from irekua_rest_api.serializers.base import IrekuaHyperlinkedModelSerializer


class SelectPermissionSerializer(IrekuaModelSerializer):
    codename = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='codename',
        queryset=Permission.objects.filter(content_type__model='collection'))

    class Meta:
        model = Permission
        fields = (
            'codename',
        )


class SelectSerializer(IrekuaModelSerializer):
    class Meta:
        model = Role
        fields = (
            'url',
            'name',
        )


class ListSerializer(IrekuaModelSerializer):
    class Meta:
        model = Role
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(IrekuaHyperlinkedModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='codename')

    class Meta:
        model = Role
        fields = (
            'url',
            'name',
            'description',
            'permissions',
            'icon',
            'modified_on',
            'created_on',
        )


class CreateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Role
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(IrekuaModelSerializer):
    class Meta:
        model = Role
        fields = (
            'description',
            'icon',
        )
