# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_models import models
from irekua_rest_api import utils
from irekua_rest_api import filters
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAuthenticated


class ModelVersionViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        utils.CustomViewSetMixin,
        GenericViewSet):
    queryset = models.ModelVersion.objects.all()  # pylint: disable=no-member
    filterset_class = filters.model_versions.Filter
    search_fields = filters.model_versions.search_fields

    permission_mapping = utils.PermissionMapping(default=IsAuthenticated)
    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.models.model_version)
