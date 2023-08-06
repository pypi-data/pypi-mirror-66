from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.created_by == user


class IsOpen(BasePermission):
    def has_object_permission(self, request, view, obj):
        annotation = obj.annotation
        item = annotation.item
        licence = item.licence

        if not licence.is_active:
            return True

        licence_type = licence.licence_type
        can_view = licence_type.can_view_annotations
        return can_view


class HasViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        annotation = obj.annotation
        item = annotation.item
        sampling_event = item.sampling_event
        collection = sampling_event.collection

        try:
            collectionuser = collection.collectionuser_set.get(user=user)
        except collection.collectionuser_set.DoesNotExist:
            return False

        role = collectionuser.role
        has_permission = role.permissions.filter(
            codename='view_collection_annotation_vote').exists()
        return has_permission
