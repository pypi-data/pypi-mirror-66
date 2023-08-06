# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsDeveloper
from irekua_rest_api.permissions import ReadOnly


class TermViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  utils.CustomViewSetMixin,
                  GenericViewSet):
    queryset = models.Term.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.terms.terms)

    permission_mapping = utils.PermissionMapping(
        default=IsDeveloper | IsAdmin | ReadOnly)
