from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase

from irekua_rest_api.serializers import institutions
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class InstitutionTestCase(BaseTestCase, APITestCase):
    serializer = institutions.CreateSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: Users.ALL_AUTHENTICATED_USERS,
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
            'institution_name': str(uuid4()),
            'institution_code': str(uuid4()),
            'subdependency': str(uuid4())
        }
        return data

    def test_update_own_institution(self):
        institution = self.create_random_object()
        other_institution = self.create_random_object()

        new_data = self.generate_random_json_data()
        new_data['country'] = 'MX'

        self.regular_user.institution = other_institution
        self.regular_user.save()

        self.client.force_authenticate(user=self.regular_user)

        url_name = self.get_url_name(Actions.UPDATE)
        url = reverse(url_name, args=[institution.pk])
        response = self.client.put(url, new_data, format='json')
        self.check_response(
            Actions.UPDATE,
            response,
            False,
            'User not from institution')

        url_name = self.get_url_name(Actions.PARTIAL_UPDATE)
        url = reverse(url_name, args=[institution.pk])
        response = self.client.patch(url, new_data, format='json')
        self.check_response(
            Actions.PARTIAL_UPDATE,
            response,
            False,
            'User not from institution')

        url_name = self.get_url_name(Actions.UPDATE)
        url = reverse(url_name, args=[other_institution.pk])
        response = self.client.put(url, new_data, format='json')
        self.check_response(
            Actions.UPDATE,
            response,
            True,
            'User from institution')

        url_name = self.get_url_name(Actions.PARTIAL_UPDATE)
        url = reverse(url_name, args=[other_institution.pk])
        response = self.client.patch(url, new_data, format='json')
        self.check_response(
            Actions.PARTIAL_UPDATE,
            response,
            True,
            'User from institution')
