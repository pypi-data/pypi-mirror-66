from rest_framework.permissions import BasePermission


class IsOwnSuggestion(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.suggested_by == user
