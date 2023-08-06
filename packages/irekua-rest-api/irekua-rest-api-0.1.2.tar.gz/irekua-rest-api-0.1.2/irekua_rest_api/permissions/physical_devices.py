from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.owner == user
