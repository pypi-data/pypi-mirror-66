from rest_framework.permissions import BasePermission


class IsOwnSuggestion(BasePermission):
    def has_permission(self, request, view):
        try:
            suggestion = view.get_object()
            user = request.user
            return suggestion.suggested_by == user
        except (AttributeError, AssertionError):
            return False
