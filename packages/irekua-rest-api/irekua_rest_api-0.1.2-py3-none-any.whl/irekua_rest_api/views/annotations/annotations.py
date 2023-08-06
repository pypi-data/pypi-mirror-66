# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers
from irekua_rest_api import filters

from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsCurator
from irekua_rest_api.permissions import IsSpecialUser
from irekua_rest_api.permissions import annotations as permissions


class AnnotationViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        utils.CustomViewSetMixin,
                        GenericViewSet):
    queryset = models.Annotation.objects.all()  # pylint: disable=E1101
    filterset_class = filters.annotations.Filter
    search_fields = filters.annotations.search_fields

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.annotations.annotations)
        .extend(
            vote=serializers.annotations.votes.CreateSerializer,
            votes=serializers.annotations.votes.ListSerializer,
            types=serializers.object_types.annotations.ListSerializer,
            add_type=serializers.object_types.annotations.CreateSerializer,
            tools=serializers.annotations.tools.ListSerializer,
            add_tool=serializers.annotations.tools.CreateSerializer,
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasUpdatePermission |
                IsCurator |
                IsAdmin
            ),
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsCreator | IsAdmin,
        ],
        'vote': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasVotePermission |
                IsCurator |
                IsAdmin
            ),
        ],
        'votes': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        'add_type': [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)

    def get_object(self):
        annotation_id = self.kwargs['pk']
        annotation = get_object_or_404(models.Annotation, pk=annotation_id)

        self.check_object_permissions(self.request, annotation)
        return annotation

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            annotation = self.get_object()
        except (KeyError, AssertionError, AttributeError):
            annotation = None

        context['annotation'] = annotation
        return context

    def get_queryset(self):
        if self.action == 'votes':
            annotation_id = self.kwargs['pk']
            return models.AnnotationVote.objects.filter(
                annotation=annotation_id)

        if self.action == 'types':
            return models.AnnotationType.objects.all()

        if self.action == 'tools':
            return models.AnnotationTool.objects.all()

        if self.action == utils.Actions.LIST:
            return self.get_list_queryset()

        return super().get_queryset()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.annotation_votes.Filter,
        search_fields=filters.annotation_votes.search_fields)
    def votes(self, request, pk=None):
        return self.list_related_object_view()

    @votes.mapping.post
    def vote(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.annotation_types.Filter,
        search_fields=filters.annotation_types.search_fields)
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.annotation_tools.Filter,
        search_fields=filters.annotation_tools.search_fields)
    def tools(self, request):
        return self.list_related_object_view()

    @tools.mapping.post
    def add_tool(self, request):
        return self.create_related_object_view()

    def get_list_queryset(self):
        user = self.request.user

        if user.is_special:
            return models.Annotation.objects.all()

        collection_type_queryset = self.get_collection_type_admin_queryset(user)
        collection_admin_queryset = self.get_collection_admin_queryset(user)
        view_pemission_queryset = self.get_view_permission_queryset(user)
        open_queryset = self.get_open_queryset()

        return open_queryset.union(collection_type_queryset,
                                   collection_admin_queryset,
                                   view_pemission_queryset)

    def get_collection_type_admin_queryset(self, user):
        return models.Annotation.objects.none()

    def get_collection_admin_queryset(self, user):
        return models.Annotation.objects.none()

    def get_view_permission_queryset(self, user):
        return models.Annotation.objects.none()

    def get_open_queryset(self):
        return models.Annotation.objects.none()
