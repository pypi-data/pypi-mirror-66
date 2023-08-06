# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAuthenticated


class SecondaryItemViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           utils.CustomViewSetMixin,
                           GenericViewSet):
    queryset = models.SecondaryItem.objects.all()  # pylint: disable=E1101

    permission_mapping = utils.PermissionMapping(default=IsAuthenticated) # TODO: Fix permissions
    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.items.secondary_items)
