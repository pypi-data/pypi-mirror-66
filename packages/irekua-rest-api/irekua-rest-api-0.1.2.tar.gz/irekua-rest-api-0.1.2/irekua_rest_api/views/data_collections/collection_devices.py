# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsSpecialUser
from irekua_rest_api.permissions import collection_devices as permissions


class CollectionDeviceViewSet(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              utils.CustomViewSetMixin,
                              GenericViewSet):
    queryset = models.CollectionDevice.objects.all() # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.data_collections.devices)

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                permissions.HasUpdatePermission |
                IsAdmin
            ),
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                IsAdmin
            ),
        ]
    })
