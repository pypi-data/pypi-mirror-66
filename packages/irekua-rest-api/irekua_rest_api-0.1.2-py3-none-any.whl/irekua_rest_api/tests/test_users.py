from uuid import uuid4

from rest_framework.test import APITestCase
from irekua_rest_api.serializers import users
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class UserTestCase(BaseTestCase, APITestCase):
    serializer = users.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.NON_AUTHENTICATED,
            Users.ADMIN,
        ],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN,
        ],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN,
        ],
        Actions.DESTROY: [
            Users.ADMIN,
        ],
    })

    @staticmethod
    def generate_random_json_data():
        data = {
            'username': str(uuid4()),
            'password': str(uuid4()),
        }
        return data
