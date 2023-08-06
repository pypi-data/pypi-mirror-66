# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
import irekua_rest_api.permissions.synonym_suggestions as permissions


class SynonymSuggestionViewSet(mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               utils.CustomViewSetMixin,
                               GenericViewSet):
    queryset = models.SynonymSuggestion.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.terms.synonym_suggestions)

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated, # TODO: Fix permissions
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin
        ]
    }, default=IsAuthenticated)
