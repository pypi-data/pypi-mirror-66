# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import filters
from irekua_rest_api import utils
from irekua_rest_api import serializers

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsDeveloper
from irekua_rest_api.permissions import IsSpecialUser
from irekua_rest_api.permissions import IsAuthenticated


class MetaCollectionViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.MetaCollection.objects.all()  # pylint: disable=E1101
    filterset_class = filters.metacollections.Filter
    search_fields = filters.metacollections.search_fields

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.data_collections.metacollections)
        .extend(
            items=serializers.items.items.ListSerializer,
            add_item=serializers.items.items.SelectSerializer,
            remove_item=serializers.items.items.SelectSerializer,
            add_curator=serializers.users.users.SelectSerializer,
            remove_curator=serializers.users.users.SelectSerializer,
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.LIST: [
            IsAuthenticated
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            IsSpecialUser
        ],
        'items': [
            IsAuthenticated,
            IsSpecialUser
        ],
        'add_curator': [
            IsAuthenticated, IsAdmin
        ],
        'remove_curator': [
            IsAuthenticated, IsAdmin
        ],
    }, default=[
        IsAuthenticated,
        IsDeveloper | IsAdmin
    ])

    def get_queryset(self):
        if self.action == 'items':
            metacollection_id = self.kwargs['pk']
            metacollection = models.MetaCollection.objects.get(pk=metacollection_id)  # pylint: disable=E1101
            return metacollection.items.all()

        return super().get_queryset()

    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        return self.add_related_object_view(models.Item, 'item')

    @action(detail=True, methods=['POST'])
    def remove_item(self, request, pk=None):
        return self.remove_related_object_view('item')

    @action(detail=True, methods=['POST'])
    def add_curator(self, request, pk=None):
        return self.add_related_object_view(models.User, 'curator')

    @action(detail=True, methods=['POST'])
    def remove_curator(self, request, pk=None):
        return self.remove_related_object_view('curator')

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def items(self, request, pk=None):
        return self.list_related_object_view()
