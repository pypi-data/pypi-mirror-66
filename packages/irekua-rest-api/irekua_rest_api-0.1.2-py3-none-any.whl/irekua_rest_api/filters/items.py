import django_filters

from irekua_database.models import Item
from .utils import BaseFilter


search_fields = (
    'item_type__name',
)


class Filter(BaseFilter):
    is_uploaded = django_filters.BooleanFilter(
        field_name='item_file',
        method='is_uploaded_filter',
        label='is uploaded')

    def is_uploaded_filter(self, queryset, name, value):
        return queryset.filter(item_file__isnull=False)

    class Meta:
        model = Item
        fields = (
            'is_uploaded',
            'item_type',
            'sampling_event_device__sampling_event__sampling_event_type',
            'sampling_event_device__sampling_event__collection',
            'sampling_event_device__sampling_event__collection__collection_type',
            'sampling_event_device__sampling_event__collection_site__site_type',
            'sampling_event_device__collection_device__physical_device__device__device_type',
            'sampling_event_device__collection_device__physical_device__device__brand',
        )
