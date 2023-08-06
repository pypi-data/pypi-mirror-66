import django_filters

from irekua_database.models import SamplingEvent
from .utils import BaseFilter


search_fields = (
    'sampling_event_type__name',
    'collection_site__site__site_type__name',
    'collection_site__site__locality',
)


class Filter(BaseFilter):
    latitude__gt = django_filters.NumberFilter(
        field_name='site.latitude',
        lookup_expr='gt')
    latitude__lt = django_filters.NumberFilter(
        field_name='site.latitude',
        lookup_expr='lt')

    longitude__gt = django_filters.NumberFilter(
        field_name='site.longitude',
        lookup_expr='gt')
    longitude__lt = django_filters.NumberFilter(
        field_name='site.longitude',
        lookup_expr='lt')

    altitude__gt = django_filters.NumberFilter(
        field_name='site.altitude',
        lookup_expr='gt')
    altitude__lt = django_filters.NumberFilter(
        field_name='site.altitude',
        lookup_expr='lt')

    started_on__gt = django_filters.NumberFilter(
        field_name='started_on',
        lookup_expr='gt')
    started_on__lt = django_filters.NumberFilter(
        field_name='started_on',
        lookup_expr='lt')

    ended_on__gt = django_filters.NumberFilter(
        field_name='ended_on',
        lookup_expr='gt')
    ended_on__lt = django_filters.NumberFilter(
        field_name='ended_on',
        lookup_expr='lt')

    class Meta:
        model = SamplingEvent
        fields = (
            'sampling_event_type__name',
            'collection_site__site_type',
            'collection_site__site__locality',
            'collection__collection_type__name',
            'collection__name',
        )
