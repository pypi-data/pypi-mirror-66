# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsDeveloper
from irekua_rest_api.permissions import IsAuthenticated


class ItemTypeViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      utils.CustomViewSetMixin,
                      GenericViewSet):
    queryset = models.ItemType.objects.all()  # pylint: disable=E1101

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.object_types.items)
        .extend(
            add_event_types=serializers.object_types.events.SelectSerializer,
            remove_event_types=serializers.object_types.events.SelectSerializer
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.RETRIEVE: IsAuthenticated,
        utils.Actions.DESTROY: IsAdmin,
    }, default=IsDeveloper | IsAdmin)

    @action(detail=True, methods=['POST'])
    def add_event_types(self, request, pk=None):
        return self.add_related_object_view(models.EventType, 'event_type')

    @action(detail=True, methods=['POST'])
    def remove_event_types(self, request, pk=None):
        return self.remove_related_object_view('event_type')
