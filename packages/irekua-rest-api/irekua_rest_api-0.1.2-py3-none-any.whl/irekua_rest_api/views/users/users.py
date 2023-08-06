# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.response import Response

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import filters
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsUnauthenticated
from irekua_rest_api.permissions import users as permissions


class UserViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  utils.CustomViewSetMixin,
                  GenericViewSet):
    queryset = models.User.objects.all()  # pylint: disable=E1101
    filterset_class = filters.users.Filter
    search_fields = filters.users.search_fields

    permission_mapping = utils.PermissionMapping({
        utils.Actions.CREATE: IsUnauthenticated,
        utils.Actions.UPDATE: [
            IsAuthenticated,
            permissions.IsSelf | IsAdmin
        ], # TODO: Fix permissions
    }, default=IsAuthenticated)

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.users.users)
        .extend(
            items=serializers.items.items.ListSerializer,
            devices=serializers.devices.physical_devices.ListSerializer,
            sites=serializers.sites.ListSerializer,
            roles=serializers.users.roles.ListSerializer,
            sampling_events=serializers.sampling_events.sampling_events.UserListSerializer,
            add_role=serializers.users.roles.CreateSerializer,
            collections=serializers.data_collections.data_collections.ListSerializer,
            institutions=serializers.users.institutions.ListSerializer,
            add_institution=serializers.users.institutions.CreateSerializer,
        ))

    def get_object(self):
        user_pk = self.kwargs['pk']
        user = get_object_or_404(models.User, pk=user_pk)

        self.check_object_permissions(self.request, user)
        return user

    def get_serializer_class(self):
        if self.action == 'retrieve':
            try:
                user = self.request.user
                viewed_user = self.get_object()

                if user == viewed_user or user.is_superuser:
                    return serializers.users.users.FullDetailSerializer
            except (AssertionError, AttributeError):
                return serializers.users.users.DetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == 'roles':
            return models.Role.objects.all()  # pylint: disable=E1101

        if self.action == 'institutions':
            return models.Institution.objects.all()  # pylint: disable=E1101

        if self.action == 'items' or self.action == 'item_locations':
            user_id = self.kwargs['pk']
            return models.Item.objects.filter(created_by=user_id)  # pylint: disable=E1101

        if self.action == 'devices':
            user_id = self.kwargs['pk']
            return models.PhysicalDevice.objects.filter(owner=user_id)  # pylint: disable=E1101

        if self.action == 'sites' or self.action == 'site_locations':
            user_id = self.kwargs['pk']
            return models.Site.objects.filter(created_by=user_id)  # pylint: disable=E1101

        if self.action == 'collections':
            user = self.get_object()
            return user.collection_users.all()

        if self.action == 'sampling_events' or self.action == 'sampling_event_locations':
            user = self.get_object()
            return user.sampling_event_created_by.all()

        return super().get_queryset()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.roles.Filter,
        search_fields=filters.roles.search_fields)
    def roles(self, request):
        return self.list_related_object_view()

    @roles.mapping.post
    def add_role(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.institutions.Filter,
        search_fields=filters.institutions.search_fields)
    def institutions(self, request):
        return self.list_related_object_view()

    @institutions.mapping.post
    def add_institution(self, request):
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
        methods=['GET'],
        filterset_class=filters.physical_devices.Filter,
        search_fields=filters.physical_devices.search_fields)
    def devices(self, request, pk=None):
        return self.list_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.sites.Filter,
        search_fields=filters.sites.search_fields)
    def sites(self, request, pk=None):
        return self.list_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.sampling_events.Filter,
        search_fields=filters.sampling_events.search_fields)
    def sampling_events(self, request, pk=None):
        return self.list_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.data_collections.Filter,
        search_fields=filters.data_collections.search_fields)
    def collections(self, request, pk=None):
        return self.list_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.sites.Filter,
        search_fields=filters.sites.search_fields)
    def site_locations(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = serializers.sites.SiteLocationSerializer(
            queryset,
            many=True,
            read_only=True)
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

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.sampling_events.Filter,
        search_fields=filters.sampling_events.search_fields)
    def sampling_event_locations(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = serializers.sites.SamplingEventLocationSerializer(
            queryset,
            many=True,
            read_only=True)
        return Response(serializer.data)
