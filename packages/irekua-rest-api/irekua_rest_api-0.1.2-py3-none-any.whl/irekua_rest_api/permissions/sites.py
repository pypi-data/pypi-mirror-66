from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        creator = obj.created_by
        return user == creator
