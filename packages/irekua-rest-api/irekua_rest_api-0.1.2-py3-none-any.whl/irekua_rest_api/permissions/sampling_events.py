from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        creator = obj.created_by
        return user == creator


class HasChangePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection
        return collection.has_permission(
            user, 'change_collection_sampling_events')


class HasViewPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection
        return collection.has_permission(
            user, 'view_collection_sampling_events')


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


class HasViewItemsPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection = obj.collection
        return collection.has_permission(
            user, 'view_collection_item')
