# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsSpecialUser
from irekua_rest_api.permissions import collection_users as permissions


class CollectionUserViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.CollectionUser.objects.all()  # pylint: disable=E1101

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(
            serializers.data_collections.users)
        .extend(
            change_role=serializers.data_collections.users.RoleSerializer
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsSelf |
                permissions.HasUpdatePermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            ),
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsSelf |
                permissions.IsInCollection |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsSelf |
                IsAdmin
            ),
        ],
        'change_role': [
            (
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
    })

    @action(detail=True, methods=['POST'])
    def change_role(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
