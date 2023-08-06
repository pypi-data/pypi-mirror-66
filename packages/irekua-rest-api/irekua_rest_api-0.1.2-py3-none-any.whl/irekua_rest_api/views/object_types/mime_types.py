# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsDeveloper
from irekua_rest_api.permissions import IsAuthenticated


class MimeTypeViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      utils.CustomViewSetMixin,
                      GenericViewSet):
    queryset = models.MimeType.objects.all()  # pylint: disable=E1101

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.object_types.mime_types))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.RETRIEVE: IsAuthenticated,
        utils.Actions.DESTROY: IsAdmin,
    }, default=IsDeveloper | IsAdmin)
