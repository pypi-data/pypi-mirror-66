from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        site = obj.site
        creator = site.created_by

        return user == creator


class HasUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection

        return collection.has_permission(
            user, 'change_collection_sites')


class HasViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection

        return collection.has_permission(
            user, 'view_collection_sites')


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
