from uuid import uuid4

from rest_framework.test import APITestCase

from irekua_database.models import User, DeviceType, Device, DeviceBrand
from irekua_database.utils import simple_JSON_schema
from irekua_rest_api.serializers import physical_devices
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class DummyRequest(object):
    def __init__(self, user):
        self.user = user


class PhysicalDevicesTestCase(BaseTestCase, APITestCase):
    serializer = physical_devices.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: Users.ALL_AUTHENTICATED_USERS,
        Actions.RETRIEVE: [
            Users.ADMIN,
        ],
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

    def setUp(self):
        super(PhysicalDevicesTestCase, self).setUp()
        self.random_user = User.objects.create(
            username=str(uuid4()),
            password=str(uuid4()))

        device_type = DeviceType.objects.create(
            name=str(uuid4()),
            description='Random device type')

        device_brand = DeviceBrand.objects.create(
            name=str(uuid4())
        )

        self.device = Device.objects.create(
            device_type=device_type,
            brand=device_brand,
            model=str(uuid4()),
            metadata_schema=simple_JSON_schema(),
            configuration_schema=simple_JSON_schema())

    def get_serializer_context(self):
        request = DummyRequest(self.random_user)
        return {'request': request}

    def generate_random_json_data(self):
        data = {
            'device': self.device.pk,
            'serial_number': str(uuid4()),
            'metadata': {},
            'bundle': False,
        }
        return data
