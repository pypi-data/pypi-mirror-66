# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from irekua_database.models import Term
from irekua_models import models
from irekua_rest_api import utils
from irekua_rest_api import filters
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAuthenticated


class ModelViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        utils.CustomViewSetMixin,
        GenericViewSet):
    queryset = models.Model.objects.all()  # pylint: disable=no-member
    filterset_class = filters.models.Filter
    search_fields = filters.models.search_fields

    permission_mapping = utils.PermissionMapping(default=IsAuthenticated)
    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.models.model)
        .extend(
            terms=serializers.terms.terms.ListSerializer,
            add_term=serializers.terms.terms.SelectSerializer)
    )

    def get_queryset(self):
        if self.action == 'terms':
            return Term.objects.filter(model=self.kwargs['pk'])

        return super().get_queryset()
