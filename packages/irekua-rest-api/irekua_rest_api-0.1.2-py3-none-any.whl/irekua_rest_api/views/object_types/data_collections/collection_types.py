# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils


class CollectionTypeViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.CollectionType.objects.all()  # pylint: disable=E1101

    permission_mapping = utils.PermissionMapping()

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.object_types.data_collections.types)
        .extend(
            administrators=serializers.object_types.data_collections.administrators.ListSerializer,  # noqa pylint: disable=C0301
            add_administrator=serializers.object_types.data_collections.administrators.CreateSerializer,  # noqa pylint: disable=C0301
            site_types=serializers.object_types.data_collections.sites.ListSerializer,  # noqa pylint: disable=C0301
            add_site_type=serializers.object_types.data_collections.sites.CreateSerializer,  # noqa pylint: disable=C0301
            annotation_types=serializers.object_types.data_collections.annotations.ListSerializer,  # noqa pylint: disable=C0301
            add_annotation_type=serializers.object_types.data_collections.annotations.CreateSerializer,  # noqa pylint: disable=C0301
            licence_types=serializers.object_types.data_collections.licences.ListSerializer,  # noqa pylint: disable=C0301
            add_licence_type=serializers.object_types.data_collections.licences.CreateSerializer,  # noqa pylint: disable=C0301
            sampling_event_types=serializers.object_types.data_collections.sampling_events.ListSerializer,  # noqa pylint: disable=C0301
            add_sampling_event_type=serializers.object_types.data_collections.sampling_events.CreateSerializer,  # noqa pylint: disable=C0301
            item_types=serializers.object_types.data_collections.items.ListSerializer,  # noqa pylint: disable=C0301
            add_item_type=serializers.object_types.data_collections.items.CreateSerializer,  # noqa pylint: disable=C0301
            event_types=serializers.object_types.data_collections.events.ListSerializer,  # noqa pylint: disable=C0301
            add_event_type=serializers.object_types.data_collections.events.CreateSerializer,  # noqa pylint: disable=C0301
            device_types=serializers.object_types.data_collections.devices.ListSerializer,  # noqa pylint: disable=C0301
            add_device_type=serializers.object_types.data_collections.devices.CreateSerializer,  # noqa pylint: disable=C0301
            roles=serializers.object_types.data_collections.roles.ListSerializer,  # noqa pylint: disable=C0301
            add_role=serializers.object_types.data_collections.roles.CreateSerializer,  # noqa pylint: disable=C0301
        ))

    def get_object(self):
        type_pk = self.kwargs['pk']
        type = get_object_or_404(models.CollectionType, pk=type_pk)

        self.check_object_permissions(self.request, type)
        return type

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            collection_type = self.get_object()
        except (KeyError, AttributeError, AssertionError):
            collection_type = None

        context['collection_type'] = collection_type
        return context

    def get_queryset(self):
        if self.action == 'site_types':
            model = models.CollectionType.site_types.through  # pylint: disable=E1101
            collection_id = self.kwargs['pk']
            return model.objects.filter(collectiontype_id=collection_id)

        if self.action == 'administrators':
            model = models.CollectionType.administrators.through  # pylint: disable=E1101
            collection_id = self.kwargs['pk']
            return model.objects.filter(collectiontype_id=collection_id)

        if self.action == 'annotation_types':
            model = models.CollectionType.annotation_types.through  # pylint: disable=E1101
            collection_id = self.kwargs['pk']
            return model.objects.filter(collectiontype_id=collection_id)

        if self.action == 'licence_types':
            model = models.CollectionType.licence_types.through  # pylint: disable=E1101
            collection_id = self.kwargs['pk']
            return model.objects.filter(collectiontype_id=collection_id)

        if self.action == 'sampling_event_types':
            model = models.CollectionType.sampling_event_types.through  # pylint: disable=E1101
            collection_id = self.kwargs['pk']
            return model.objects.filter(collectiontype_id=collection_id)

        if self.action == 'item_types':
            collection_id = self.kwargs['pk']
            return models.CollectionItemType.objects.filter(  # pylint: disable=E1101
                collection_type=collection_id)

        if self.action == 'event_types':
            model = models.CollectionType.event_types.through  # pylint: disable=E1101
            collection_id = self.kwargs['pk']
            return model.objects.filter(collectiontype_id=collection_id)

        if self.action == 'device_types':
            collection_id = self.kwargs['pk']
            return models.CollectionDeviceType.objects.filter(  # pylint: disable=E1101
                collection_type=collection_id)

        if self.action == 'roles':
            collection_id = self.kwargs['pk']
            return models.CollectionRole.objects.filter(  # pylint: disable=E1101
                collection_type=collection_id)

        return super().get_queryset()

    @action(detail=True, methods=['GET'])
    def site_types(self, request, pk=None):
        return self.list_related_object_view()

    @site_types.mapping.post
    def add_site_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def administrators(self, request, pk=None):
        return self.list_related_object_view()

    @administrators.mapping.post
    def add_administrator(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def annotation_types(self, request, pk=None):
        return self.list_related_object_view()

    @annotation_types.mapping.post
    def add_annotation_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def licence_types(self, request, pk=None):
        return self.list_related_object_view()

    @licence_types.mapping.post
    def add_licence_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def sampling_event_types(self, request, pk=None):
        return self.list_related_object_view()

    @sampling_event_types.mapping.post
    def add_sampling_event_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def item_types(self, request, pk=None):
        return self.list_related_object_view()

    @item_types.mapping.post
    def add_item_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def event_types(self, request, pk=None):
        return self.list_related_object_view()

    @event_types.mapping.post
    def add_event_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def device_types(self, request, pk=None):
        return self.list_related_object_view()

    @device_types.mapping.post
    def add_device_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def roles(self, request, pk=None):
        return self.list_related_object_view()

    @roles.mapping.post
    def add_role(self, request, pk=None):
        return self.create_related_object_view()
