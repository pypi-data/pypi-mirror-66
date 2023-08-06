from irekua_database.models import Device
from .utils import BaseFilter


search_fields = (
    'brand__name',
    'model',
    'device_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = Device
        fields = (
            'brand__name',
            'model',
            'device_type__name',
        )
