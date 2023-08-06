from rest_framework.permissions import BasePermission
from irekua_permissions.annotations import (
    annotations as annotation_permissions)


class CanAnnotate(BasePermission):
    def has_permission(self, request, view):
        item = view.get_object()
        user = request.user
        return annotation_permissions.create(user, item=item)


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        return user == obj.created_by


class HasUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(user, 'change_collection_item')


class HasViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(user, 'view_collection_item')


class HasViewAnnotationsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(user, 'view_collection_annotations')

class HasDownloadPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(user, 'download_collection_items')


class HasAddAnnotationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.has_permission(user, 'add_collection_annotation')


class IsCollectionAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection

        return collection.is_admin(user)


class IsCollectionTypeAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        sampling_event = obj.sampling_event_device.sampling_event
        collection = sampling_event.collection
        collection_type = collection.collection_type

        return collection_type.is_admin(user)


class ItemIsOpenToView(BasePermission):
    def has_object_permission(self, request, view, obj):
        licence = obj.licence

        if not licence.is_active:
            return True

        licence_type = licence.licence_type
        return licence_type.can_view


class ItemIsOpenToDownload(BasePermission):
    def has_object_permission(self, request, view, obj):
        licence = obj.licence

        if not licence.is_active:
            return True

        licence_type = licence.licence_type
        return licence_type.can_download


class ItemIsOpenToAnnotate(BasePermission):
    def has_object_permission(self, request, view, obj):
        licence = obj.licence

        if not licence.is_active:
            return True

        licence_type = licence.licence_type
        return licence_type.can_annotate


class ItemIsOpenToViewAnnotations(BasePermission):
    def has_object_permission(self, request, view, obj):
        licence = obj.licence

        if not licence.is_active:
            return True

        licence_type = licence.licence_type
        return licence_type.can_view_annotation
