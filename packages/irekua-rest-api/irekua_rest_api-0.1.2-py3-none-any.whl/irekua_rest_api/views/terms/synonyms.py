# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsCurator
from irekua_rest_api.permissions import ReadOnly


class SynonymViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     utils.CustomViewSetMixin,
                     GenericViewSet):
    queryset = models.Synonym.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.terms.synonyms)

    permission_mapping = utils.PermissionMapping(
        default=IsAdmin | IsCurator | ReadOnly)
