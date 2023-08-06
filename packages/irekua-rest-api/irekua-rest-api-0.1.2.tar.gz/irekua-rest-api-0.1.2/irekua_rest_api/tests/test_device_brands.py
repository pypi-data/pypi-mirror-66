from uuid import uuid4

from rest_framework.test import APITestCase
from irekua_rest_api.serializers import device_brands
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class DeviceBrandTestCase(BaseTestCase, APITestCase):
    serializer = device_brands.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: Users.ALL_AUTHENTICATED_USERS,
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN, Users.CURATOR],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN, Users.CURATOR],
        Actions.DESTROY: [
            Users.ADMIN, Users.CURATOR],
    })

    @staticmethod
    def generate_random_json_data():
        data = {
            'name': str(uuid4()),
        }
        return data
