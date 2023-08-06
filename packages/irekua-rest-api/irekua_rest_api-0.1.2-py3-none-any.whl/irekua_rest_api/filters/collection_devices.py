from irekua_database.models import CollectionDevice
from .utils import BaseFilter


search_fields = (
    'physical_device__device__model',
    'physical_device__device__brand__name',
    'physical_device__device__device_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = CollectionDevice
        fields = (
            'physical_device__device__model',
            'physical_device__device__brand__name',
            'physical_device__device__device_type__name',
            'physical_device__bundle',
            'physical_device__created_by__username',
            'physical_device__created_by__first_name',
            'physical_device__created_by__last_name',
            'internal_id',
        )
