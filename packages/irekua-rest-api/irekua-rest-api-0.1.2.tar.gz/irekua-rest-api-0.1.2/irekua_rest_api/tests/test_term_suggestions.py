from uuid import uuid4

from rest_framework.test import APITestCase

from irekua_database.models import User, TermType
from irekua_database.utils import simple_JSON_schema
from irekua_rest_api.serializers import term_suggestions
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class DummyRequest(object):
    def __init__(self, user):
        self.user = user


class TermSuggestionTestCase(BaseTestCase, APITestCase):
    serializer = term_suggestions.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: Users.ALL_AUTHENTICATED_USERS,
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN],
        Actions.DESTROY: [
            Users.ADMIN],
    })

    def setUp(self):
        super(TermSuggestionTestCase, self).setUp()
        self.random_user = User.objects.create(
            username=str(uuid4()),
            password=str(uuid4()))
        self.term_type = TermType.objects.create(
            name=str(uuid4()),
            description='Random term type',
            is_categorical=True,
            metadata_schema=simple_JSON_schema(),
            synonym_metadata_schema=simple_JSON_schema())

    def get_serializer_context(self):
        request = DummyRequest(user=self.random_user)
        return {'request': request}

    def generate_random_json_data(self):
        data = {
            'term_type': self.term_type.pk,
            'value': str(uuid4()),
            'description': 'Random term suggestion',
            'metadata': {}
        }
        return data
