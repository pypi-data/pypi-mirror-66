from irekua_database.models import PhysicalDevice
from .utils import BaseFilter


search_fields = (
    'device__brand__name',
    'device__model',
    'device__device_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = PhysicalDevice
        fields = (
            'device__brand__name',
            'device__model',
            'device__device_type__name',
            'created_by__username',
            'created_by__first_name'
        )
