from uuid import uuid4

from rest_framework.test import APITestCase
from irekua_rest_api.serializers import roles
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class RoleTestCase(BaseTestCase, APITestCase):
    serializer = roles.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
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
            'name': str(uuid4()),
            'description': 'Random Role',
        }
        return data
