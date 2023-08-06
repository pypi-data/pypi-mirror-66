from uuid import uuid4

from rest_framework.test import APITestCase

from irekua_database.models import TermType
from irekua_database.utils import simple_JSON_schema
from irekua_rest_api.serializers import event_types

from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class EventTypeTestCase(BaseTestCase, APITestCase):
    serializer = event_types.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.ADMIN],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN],
        Actions.DESTROY: [
            Users.ADMIN],
    })

    @staticmethod
    def generate_random_json_data():
        data = {
            'name': str(uuid4()),
            'description': 'Random event type',
        }
        return data

    def setUp(self):
        super(EventTypeTestCase, self).setUp()

        self.event_type = self.create_random_object()
        self.term_type = TermType.objects.create(
            name=str(uuid4()),
            description='random term type',
            is_categorical=True,
            metadata_schema=simple_JSON_schema(),
            synonym_metadata_schema=simple_JSON_schema())
