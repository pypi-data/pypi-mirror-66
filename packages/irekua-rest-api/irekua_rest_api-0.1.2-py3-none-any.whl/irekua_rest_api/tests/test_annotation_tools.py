from uuid import uuid4
from random import randint

from rest_framework.test import APITestCase
from irekua_database.utils import simple_JSON_schema
from irekua_rest_api.serializers import annotation_tools
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class AnnotationToolTestCase(BaseTestCase, APITestCase):
    serializer = annotation_tools.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.ADMIN,
            Users.DEVELOPER],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN,
            Users.DEVELOPER],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN,
            Users.DEVELOPER],
        Actions.DESTROY: [
            Users.ADMIN,
            Users.DEVELOPER],
    })

    @staticmethod
    def generate_random_json_data():
        data = {
            'name': str(uuid4()),
            'version': randint(1, 10),
            'description': 'Random Annotation Tool',
            'configuration_schema': simple_JSON_schema()
        }
        return data
