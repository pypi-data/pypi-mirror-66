# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import ReadOnly
from irekua_rest_api.permissions import term_suggestions as permissions


class TermSuggestionViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.TermSuggestion.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.terms.suggestions)

    permission_mapping = utils.PermissionMapping(
        default=permissions.IsOwnSuggestion | IsAdmin | ReadOnly)
