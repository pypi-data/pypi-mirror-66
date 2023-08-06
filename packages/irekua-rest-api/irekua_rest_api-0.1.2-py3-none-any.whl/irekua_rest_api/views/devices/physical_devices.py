# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import physical_devices as permissions
from irekua_rest_api.permissions import ReadOnly


class PhysicalDeviceViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):

    queryset = models.PhysicalDevice.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.devices.physical_devices)
    permission_mapping = utils.PermissionMapping(
        default=permissions.IsOwner | IsAdmin | ReadOnly)
