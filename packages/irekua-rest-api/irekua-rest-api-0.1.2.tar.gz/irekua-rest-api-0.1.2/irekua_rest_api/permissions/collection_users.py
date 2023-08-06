from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection_user = obj.user
        return user == collection_user


class HasUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection

        return collection.has_permission(
            user, 'change_collection_users')


class IsCollectionAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection
        return collection.is_admin(user)


class IsCollectionTypeAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection
        collection_type = collection.collection_type

        return collection_type.is_admin(user)


class IsInCollection(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection
        return collection.has_user(user)
