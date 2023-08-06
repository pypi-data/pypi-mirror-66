from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.created_by == user


class IsCollectionAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        item = obj.item
        sampling_event = item.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.is_admin(user)


class IsCollectionTypeAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        item = obj.item
        sampling_event = item.sampling_event_device.sampling_event
        collection = sampling_event.collection
        collection_type = collection.collection_type

        return collection_type.is_admin(user)


class HasUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        item = obj.item
        sampling_event = item.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(
            user, 'change_collection_annotations')


class HasViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        item = obj.item
        sampling_event = item.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(
            user, 'view_collection_annotations')


class HasVotePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        item = obj.item
        sampling_event = item.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(
            user, 'add_collection_annotation_vote')
