# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsDeveloper
from irekua_rest_api.permissions import ReadOnly


class EntailmentTypeViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.EntailmentType.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.object_types.entailments)

    permission_mapping = utils.PermissionMapping(
        default=IsDeveloper | IsAdmin | ReadOnly)
