from uuid import uuid4

from rest_framework.test import APITestCase

from irekua_database.models import User
from irekua_rest_api.serializers import metacollections
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class DummyRequest(object):
    def __init__(self, user):
        self.user = user


class MetaCollectionTestCase(BaseTestCase, APITestCase):
    serializer = metacollections.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.ADMIN,
            Users.DEVELOPER,
            Users.MODEL,
        ],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN,
            Users.DEVELOPER,
            Users.MODEL,
        ],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN,
            Users.DEVELOPER,
            Users.MODEL,
        ],
        Actions.DESTROY: [
            Users.ADMIN,
            Users.DEVELOPER,
            Users.MODEL,
        ],
    })

    def setUp(self):
        super(MetaCollectionTestCase, self).setUp()
        self.random_user = User.objects.create(
            username=str(uuid4()),
            password=str(uuid4()))

    def get_serializer_context(self):
        request = DummyRequest(self.random_user)
        return {'request': request}

    @staticmethod
    def generate_random_json_data():
        data = {
            'name': str(uuid4()),
            'description': 'Random Role',
        }
        return data
