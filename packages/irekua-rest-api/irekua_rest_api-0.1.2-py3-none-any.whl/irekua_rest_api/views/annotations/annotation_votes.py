# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsSpecialUser
from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import annotation_votes as permissions


class AnnotationVoteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.AnnotationVote.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.annotations.votes)

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            permissions.IsCreator | IsAdmin,
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.HasViewPermission |
                permissions.IsCreator |
                permissions.IsOpen |
                IsSpecialUser
            ),
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsCreator | IsAdmin,
        ],
    })
