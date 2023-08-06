# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import filters
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsSpecialUser
import irekua_rest_api.permissions.sampling_events as permissions


class SamplingEventViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           utils.CustomViewSetMixin,
                           GenericViewSet):
    queryset = models.SamplingEvent.objects.all()  # pylint: disable=E1101
    search_fields = filters.sampling_events.search_fields
    filterset_class = filters.sampling_events.Filter

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.sampling_events.sampling_events)
        .extend(
            items=serializers.items.items.ListSerializer,
            devices=serializers.sampling_events.devices.ListSerializer,
            add_device=serializers.sampling_events.devices.CreateSerializer,
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasChangePermissions |
                IsAdmin
            )
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermissions |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
        utils.Actions.LIST: [
            IsAuthenticated,
        ],
        'items': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewItemsPermissions |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
    })

    def get_object(self):
        sampling_event_pk = self.kwargs['pk']
        sampling_event = get_object_or_404(
            models.SamplingEvent,
            pk=sampling_event_pk)

        self.check_object_permissions(self.request, sampling_event)
        return sampling_event

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event = self.get_object()
        except (KeyError, AssertionError, AttributeError):
            sampling_event = None

        context['sampling_event'] = sampling_event
        return context

    def get_queryset(self):
        if self.action == 'devices':
            object_id = self.kwargs['pk']
            return models.SamplingEventDevice.objects.filter(sampling_event=object_id)  # pylint: disable=E1101

        if self.action == 'items' or self.action == 'item_locations':
            object_id = self.kwargs['pk']
            return models.Item.objects.filter(  # pylint: disable=E1101
                sampling_event_device__sampling_event=object_id)

        return super().get_queryset()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.sampling_event_devices.Filter,
        search_fields=filters.sampling_event_devices.search_fields)
    def devices(self, request, pk=None):
        return self.list_related_object_view()

    @devices.mapping.post
    def add_device(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def items(self, request, pk=None):
        return self.list_related_object_view()

    @action(
        detail=True,
        methods=['GET'])
    def location(self, request, pk=None):
        sampling_event = self.get_object()
        serializer = serializers.sites.SamplingEventLocationSerializer(
            [sampling_event],
            many=True)

        return Response(serializer.data)

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def item_locations(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = serializers.sites.ItemLocationSerializer(
            queryset,
            many=True,
            read_only=True)
        return Response(serializer.data)
