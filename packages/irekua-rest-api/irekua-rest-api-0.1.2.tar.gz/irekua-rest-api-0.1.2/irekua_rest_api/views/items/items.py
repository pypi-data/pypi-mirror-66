# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import filters
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsCurator
from irekua_rest_api.permissions import IsModel
from irekua_rest_api.permissions import IsSpecialUser
from irekua_rest_api.permissions import items as permissions


class ItemViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  utils.CustomViewSetMixin,
                  GenericViewSet):
    queryset = models.Item.objects.all()  # pylint: disable=E1101
    filterset_class = filters.items.Filter
    search_fields = filters.items.search_fields

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.items.items)
        .extend(
            annotations=serializers.annotations.annotations.ListSerializer,
            add_annotation=serializers.annotations.annotations.CreateSerializer,
            types=serializers.object_types.items.ListSerializer,
            add_type=serializers.object_types.items.CreateSerializer,
            download=serializers.items.items.DownloadSerializer,
            upload=serializers.items.items.DownloadSerializer,
            tags=serializers.items.tags.ListSerializer,
            add_tag=serializers.items.tags.CreateSerializer,
            tag_item=serializers.items.tags.SelectSerializer,
            untag_item=serializers.items.tags.SelectSerializer,
            event_types=serializers.object_types.events.ListSerializer,
            add_event_type=serializers.object_types.events.CreateSerializer,
            secondary_items=serializers.items.secondary_items.ListSerializer,
            add_secondary_item=serializers.items.secondary_items.CreateSerializer,
        ))
    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasUpdatePermission |
                IsAdmin
            )
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToView |
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
        'annotations': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewAnnotationsPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToViewAnnotations |
                IsSpecialUser
            )
        ],
        'add_annotation': [
            permissions.CanAnnotate,
        ],
        'tag_item': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsCurator |
                IsAdmin
            )
        ],
        'remove_tag': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsCurator |
                IsAdmin
            )
        ],
        'upload': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
        'download': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasDownloadPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToDownload |
                IsSpecialUser
            )
        ],
        'add_type': [IsAuthenticated, IsAdmin],
        'add_event_type': [IsAuthenticated, IsAdmin],
        'secondary_items': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToView |
                IsSpecialUser
            )
        ],
        'add_secondary_item': [
            IsAuthenticated,
            (
                permissions.IsCreator | # TODO: Add correct permissions
                IsSpecialUser
            )
        ]
    }, default=IsAuthenticated)

    def get_object(self):
        item_id = self.kwargs['pk']
        item = get_object_or_404(models.Item, pk=item_id)

        self.check_object_permissions(self.request, item)
        return item

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            item = self.get_object()
        except (KeyError, AssertionError, AttributeError):
            item = None

        context['item'] = item
        return context

    def get_queryset(self):
        if self.action == 'list':
            return self.get_list_queryset()

        if self.action == 'tags':
            return models.Tag.objects.all()  # pylint: disable=E1101

        if self.action == 'annotations':
            item_id = self.kwargs['pk']
            return models.Annotation.objects.filter(item=item_id)  # pylint: disable=E1101

        if self.action == 'secondary_items':
            item_id = self.kwargs['pk']
            return models.SecondaryItem.objects.filter(item=item_id)  # pylint: disable=E1101

        if self.action == 'types':
            return models.ItemType.objects.all()  # pylint: disable=E1101

        if self.action == 'event_types':
            return models.EventType.objects.all()  # pylint: disable=E1101

        return super().get_queryset()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.tags.Filter,
        search_fields=filters.tags.search_fields)
    def tags(self, request):
        return self.list_related_object_view()

    @tags.mapping.post
    def add_tag(self, request):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.annotations.Filter,
        search_fields=filters.annotations.search_fields)
    def annotations(self, request, pk=None):
        return self.list_related_object_view()

    @annotations.mapping.post
    def add_annotation(self, request, pk=None):
        try:
            return self.create_related_object_view()
        except Exception as e:
            print(e)

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.secondary_items.Filter,
        search_fields=filters.secondary_items.search_fields)
    def secondary_items(self, request, pk=None):
        return self.list_related_object_view()

    @secondary_items.mapping.post
    def add_secondary_item(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.item_types.Filter,
        search_fields=filters.item_types.search_fields)
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.event_types.Filter,
        search_fields=filters.event_types.search_fields)
    def event_types(self, request):
        return self.list_related_object_view()

    @event_types.mapping.post
    def add_event_type(self, request):
        return self.create_related_object_view()

    @action(detail=True, methods=['POST'])
    def tag_item(self, request, pk=None):
        return self.add_related_object_view(models.Tag, 'tag')

    @action(detail=True, methods=['POST'])
    def untag_item(self, request, pk=None):
        return self.remove_related_object_view('tag')

    @action(detail=True, methods=['POST'])
    def upload(self, request, pk=None):
        item = self.get_object()

        if item.item_file.name != '':
            return Response(
                'File previously uploaded',
                status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(item, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response('Invalid file', status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response('File uploaded', status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        item = self.get_object()

        if item.item_file.name == '':
            return Response(
                'File not uploaded to server',
                status=status.HTTP_404_NOT_FOUND)

        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        serializer = serializer_class(item, context=context)

        url = serializer.data['item_file']
        return redirect(url)

    @action(
        detail=True,
        methods=['GET'])
    def location(self, request, pk=None):
        item = self.get_object()
        serializer = serializers.sites.ItemLocationSerializer(
            [item],
            many=True)
        return Response(serializer.data)

    def get_list_queryset(self):
        try:
            user = self.request.user
        except AttributeError:
            return models.Item.objects.none()  # pylint: disable=E1101

        is_special_user = (
            user.is_superuser |
            user.is_curator |
            user.is_model |
            user.is_developer
        )
        if is_special_user:
            return self.get_full_queryset()

        return self.get_normal_queryset(user)

    def get_normal_queryset(self, user):
        is_open = (
            Q(licence__is_active=False) |
            Q(licence__licence_type__can_view=True)
        )
        is_owner = Q(created_by=user.pk)

        perm = Permission.objects.get(codename='view_collection_items')
        collections_with_permission = (
            models.CollectionUser.objects  # pylint: disable=E1101
            .filter(
                user=user.pk,
                role__in=perm.role_set.all()
            ).values('collection')
        )
        # TODO
        # Check that this query is working

        is_in_allowed_collection = Q(
            sampling_event_device__sampling_event__collection__in=collections_with_permission)

        filter_query = (
            is_open |
            is_owner |
            is_in_allowed_collection
        )

        queryset = models.Item.objects.filter(filter_query)  # pylint: disable=E1101
        return queryset

    def get_full_queryset(self):
        return models.Item.objects.all()  # pylint: disable=E1101
