from abc import ABCMeta
from uuid import uuid4
from six import add_metaclass

from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS
from django.urls import reverse
from django.contrib.auth.models import User

from irekua_database.models import User
from irekua_database.tests.test_data_collections import create_simple_collection
from irekua_database.tests.test_collection_roles import create_simple_role


def create_or_get_user(
        is_superuser=None,
        is_developer=None,
        is_curator=None,
        is_model=None):

    user, _ = User.objects.get_or_create(
        username=uuid4(),
        defaults=dict(
            password=uuid4(),
            is_superuser=is_superuser,
            is_developer=is_developer,
            is_curator=is_curator,
            is_model=is_model)
    )

    return user


class Users:
    NON_AUTHENTICATED = 'non authenticated'
    USER = 'user'
    ADMIN = 'admin'
    MODEL = 'model'
    DEVELOPER = 'developer'
    CURATOR = 'curator'
    COLLECTION_USER = 'collection user'

    ALL_USERS = [
        NON_AUTHENTICATED,
        USER,
        ADMIN,
        MODEL,
        DEVELOPER,
        CURATOR,
        COLLECTION_USER,
    ]

    ALL_AUTHENTICATED_USERS = [
        USER,
        ADMIN,
        MODEL,
        DEVELOPER,
        CURATOR,
        COLLECTION_USER,
    ]


class Actions:
    LIST = 'list'
    CREATE = 'create'
    RETRIEVE = 'retrieve'
    UPDATE = 'update'
    PARTIAL_UPDATE = 'partial_update'
    DESTROY = 'destroy'

    ALL_ACTIONS = [
        LIST,
        CREATE,
        RETRIEVE,
        UPDATE,
        PARTIAL_UPDATE,
        DESTROY
    ]

    METHOD_MAPPING = {
        LIST: 'get',
        CREATE: 'post',
        RETRIEVE: 'get',
        UPDATE: 'put',
        PARTIAL_UPDATE: 'patch',
        DESTROY: 'delete'
    }

    STATUS_CODE_MAPPING = {
        LIST: status.HTTP_200_OK,
        CREATE: status.HTTP_201_CREATED,
        RETRIEVE: status.HTTP_200_OK,
        UPDATE: status.HTTP_200_OK,
        PARTIAL_UPDATE: status.HTTP_200_OK,
        DESTROY: status.HTTP_204_NO_CONTENT,
    }


def create_permission_mapping_from_lists(permission_lists):
    permission_mapping = {}

    for action in permission_lists:
        permission_mapping[action] = {}

        permission_list = permission_lists[action]
        for user_type in Users.ALL_USERS:
            permission_mapping[action][user_type] = (
                user_type in permission_list)

    return permission_mapping


@add_metaclass(ABCMeta)
class BaseTestCase(object):
    VIEW_NAME_MAPPING = {
        Actions.LIST: 'list',
        Actions.CREATE: 'list',
        Actions.RETRIEVE: 'detail',
        Actions.UPDATE: 'detail',
        Actions.PARTIAL_UPDATE: 'detail',
        Actions.DESTROY: 'detail'
    }

    @property
    def serializer(self):
        raise NotImplementedError

    @property
    def permissions(self):
        raise NotImplementedError

    @staticmethod
    def generate_random_json_data():
        raise NotImplementedError

    def setUp(self):
        self.admin_user = create_or_get_user(
            is_superuser=True,
            is_developer=False,
            is_curator=False,
            is_model=False)

        self.regular_user = create_or_get_user(
            is_superuser=False,
            is_developer=False,
            is_curator=False,
            is_model=False)

        self.model_user = create_or_get_user(
            is_superuser=False,
            is_developer=False,
            is_curator=False,
            is_model=True)

        self.developer_user = create_or_get_user(
            is_superuser=False,
            is_developer=True,
            is_curator=False,
            is_model=False)

        self.curator_user = create_or_get_user(
            is_superuser=False,
            is_developer=False,
            is_curator=True,
            is_model=False)

        self.collection = create_simple_collection()
        self.role = create_simple_role()
        self.collection.collection_type.add_role(self.role)

        self.collection_user = create_or_get_user(
            is_superuser=False,
            is_developer=False,
            is_curator=False,
            is_model=False)

        self.collection.add_user(
            self.collection_user,
            role=self.role,
            metadata={})

    def change_user(self, usertype):
        if usertype is Users.NON_AUTHENTICATED:
            self.client.force_authenticate()
            return

        mapping = {
            Users.USER: self.regular_user,
            Users.ADMIN: self.admin_user,
            Users.MODEL: self.model_user,
            Users.CURATOR: self.curator_user,
            Users.DEVELOPER: self.developer_user,
            Users.COLLECTION_USER: self.collection_user
        }

        self.client.force_authenticate(user=mapping[usertype])

    def check_response(self, action, response, has_permission, user_type):
        if not has_permission:
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
                msg=user_type)
        else:
            status_code = Actions.STATUS_CODE_MAPPING[action]
            self.assertEqual(response.status_code, status_code, msg=user_type)

    def check_permissions_for_action_and_users(self, action, permissions):
        method_name = self.get_http_method(action)
        method = getattr(self.client, method_name)
        url_name = self.get_url_name(action)

        for user_type in Users.ALL_USERS:

            if 'list' in url_name:
                url = reverse(url_name)
            else:
                sample_object = self.create_random_object()
                url = reverse(url_name, args=[sample_object.pk])

            self.change_user(user_type)
            if method_name.upper() in SAFE_METHODS:
                response = method(url)
            else:
                random_data = self.generate_random_json_data()
                response = method(url, random_data, format='json')

            self.check_response(
                action,
                response,
                permissions[user_type],
                user_type)

    @staticmethod
    def get_http_method(action):
        return Actions.METHOD_MAPPING[action]

    def get_serializer_context(self):
        return {}

    def create_random_object(self):
        context = self.get_serializer_context()
        data = self.generate_random_json_data()
        serializer_instance = self.serializer(
            data=data,
            context=context)
        if serializer_instance.is_valid():
            random_object = serializer_instance.save()
            return random_object
        else:
            raise serializers.ValidationError(serializer_instance.errors)

    def get_class_name(self):
        return self.serializer.Meta.model.__name__.lower()

    def get_url_name(self, action, view_name=None):
        class_name = self.get_class_name()
        base_url = 'rest-api:{class_name}-{view_name}'

        if view_name is None:
            view_name = self.VIEW_NAME_MAPPING[action]

        url_name = base_url.format(
            class_name=class_name,
            view_name=view_name)

        return url_name

    def test_list(self):
        action = Actions.LIST
        permissions = self.permissions[action]

        self.check_permissions_for_action_and_users(action, permissions)

    def test_create(self):
        action = Actions.CREATE
        permissions = self.permissions[action]

        self.check_permissions_for_action_and_users(action, permissions)

    def test_retrieve(self):
        action = Actions.RETRIEVE
        permissions = self.permissions[action]

        self.check_permissions_for_action_and_users(action, permissions)

    def test_update(self):
        action = Actions.UPDATE
        permissions = self.permissions[action]

        self.check_permissions_for_action_and_users(action, permissions)

    def test_partial_update(self):
        action = Actions.PARTIAL_UPDATE
        permissions = self.permissions[action]

        self.check_permissions_for_action_and_users(action, permissions)

    def test_destroy(self):
        action = Actions.DESTROY
        permissions = self.permissions[action]

        self.check_permissions_for_action_and_users(action, permissions)
