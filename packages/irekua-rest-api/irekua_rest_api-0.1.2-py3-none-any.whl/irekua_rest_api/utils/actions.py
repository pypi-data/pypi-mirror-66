# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class Actions(object):
    LIST = 'list'
    UPDATE = 'update'
    PARTIAL_UPDATE = 'partial_update'
    METADATA = 'metadata'
    CREATE = 'create'
    DESTROY = 'destroy'
    RETRIEVE = 'retrieve'

    DEFAULT_ACTIONS = [
        LIST,
        UPDATE,
        PARTIAL_UPDATE,
        METADATA,
        CREATE,
        RETRIEVE,
        DESTROY,
    ]


class AdditionalActionsMixin(object):
    def list_related_object_view(self, queryset=None):
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_related_object(
            self,
            queryset,
            pk_field='pk',
            extra=None):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        extra_dict = {}
        if extra is not None:
            for extra_value in extra:
                extra_dict[extra_value] = (
                    serializer.validated_data.pop(extra_value))

        _, pk = serializer.validated_data.popitem()

        if isinstance(pk, Model):
            return pk, extra_dict

        query = {pk_field: pk}
        related_object = get_object_or_404(
            queryset,
            **query)

        return related_object, extra_dict

    def create_related_object_view(self, extra=None):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        extra_dict = {}
        if extra is not None:
            for extra_value in extra:
                extra_dict[extra_value] = (
                    serializer.validated_data.pop(extra_value))

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_related_object_view(
            self,
            model,
            name,
            pk_field='pk',
            extra=None):
        related_object, extra_dict = self.get_related_object(
            model,
            extra=extra,
            pk_field=pk_field)

        view_object = self.get_object()
        method_name = 'add_{name}'.format(name=name)
        method = getattr(view_object, method_name)
        method(related_object, **extra_dict)
        return Response(status=status.HTTP_200_OK)

    def remove_related_object_view(
            self,
            name,
            pk_field='pk',
            many=True):
        view_object = self.get_object()
        suffix = 's' if many else '_set'
        related_manager_name = '{name}{suffix}'.format(
            name=name,
            suffix=suffix)
        related_objects = getattr(view_object, related_manager_name).all()

        related_object, _ = self.get_related_object(
            related_objects,
            pk_field=pk_field)

        method_name = 'remove_{name}'.format(name=name)
        method = getattr(view_object, method_name)
        method(related_object)
        return Response(status=status.HTTP_200_OK)
