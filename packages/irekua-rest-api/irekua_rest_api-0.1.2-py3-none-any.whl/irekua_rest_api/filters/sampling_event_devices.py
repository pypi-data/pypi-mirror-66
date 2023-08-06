from irekua_database.models import SamplingEventDevice
from .utils import BaseFilter


search_fields = (
    'collection_device__physical_device__device__brand__name',
    'collection_device__physical_device__device__model',
    'collection_device__physical_device__device__device_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = SamplingEventDevice
        fields = (
            'collection_device__physical_device__device__brand__name',
            'collection_device__physical_device__device__model',
            'collection_device__physical_device__device__device_type__name',
            'collection_device__physical_device__created_by__username',
            'collection_device__physical_device__created_by__first_name',
            'created_by__username',
            'created_by__first_name',
            'created_by__last_name',
            'modified_by__username',
            'modified_by__first_name',
            'modified_by__last_name',
            'licence__licence_type__name',
            'licence__is_active',
            'licence__licence_type__can_view',
            'licence__licence_type__can_download',
            'licence__licence_type__can_view_annotations',
            'licence__licence_type__can_annotate',
            'licence__licence_type__can_vote_annotations',
        )
