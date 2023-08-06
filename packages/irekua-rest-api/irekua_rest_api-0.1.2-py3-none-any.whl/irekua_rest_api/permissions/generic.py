from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS


class ReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super().has_permission(request, view)
        if not is_auth:
            return False

        return request.method in SAFE_METHODS


class IsUnauthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not super().has_permission(request, view)


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_developer


class IsModel(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_model


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_curator


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class IsSpecialUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser | user.is_curator | user.is_model | user.is_developer
