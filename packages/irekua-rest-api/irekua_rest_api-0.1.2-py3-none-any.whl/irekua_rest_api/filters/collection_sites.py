import django_filters

from irekua_database.models import CollectionSite
from .utils import BaseFilter


search_fields = (
    'site__name',
    'site_type',
    'site__locality',
)


class Filter(BaseFilter):
    latitude__gt = django_filters.NumberFilter(
        field_name='site__latitude',
        lookup_expr='gt')
    latitude__lt = django_filters.NumberFilter(
        field_name='site__latitude',
        lookup_expr='lt')

    longitude__gt = django_filters.NumberFilter(
        field_name='site__longitude',
        lookup_expr='gt')
    longitude__lt = django_filters.NumberFilter(
        field_name='site__longitude',
        lookup_expr='lt')

    altitude__gt = django_filters.NumberFilter(
        field_name='site__altitude',
        lookup_expr='gt')
    altitude__lt = django_filters.NumberFilter(
        field_name='site__altitude',
        lookup_expr='lt')

    class Meta:
        model = CollectionSite
        fields = (
            'site__name',
            'site_type',
            'site__locality',
            'site__created_by',
            'created_by',
            'internal_id',
        )
