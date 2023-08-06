from .actions import Actions
from .actions import AdditionalActionsMixin
from .serializers import SerializerMapping
from .serializers import SerializerMappingMixin
from .permissions import PermissionMapping
from .permissions import PermissionMappingMixin


class CustomViewSetMixin(SerializerMappingMixin,
                         PermissionMappingMixin,
                         AdditionalActionsMixin):
    pass


__all__ = [
    'SerializerMapping',
    'PermissionMapping',
    'CustomViewSetMixin',
]
