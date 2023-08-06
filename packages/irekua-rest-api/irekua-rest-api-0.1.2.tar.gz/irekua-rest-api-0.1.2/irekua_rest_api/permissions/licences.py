from rest_framework.permissions import BasePermission


class IsSigner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        signer = obj.signed_by
        return user == signer
