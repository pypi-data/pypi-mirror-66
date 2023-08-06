from rest_framework.permissions import BasePermission


class IsFromInstitution(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.has_user(user)
