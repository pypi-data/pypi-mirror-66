from irekua_database.models import SamplingEventType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = SamplingEventType
        fields = (
            'name',
            'restrict_device_types',
            'restrict_site_types',
        )
