from django.utils.translation import gettext as _
import django_filters

from irekua_database.models import Site

from .utils import BaseFilter


search_fields = (
    'name',
    'locality',
)


class SiteBaseFilter(BaseFilter):
    latitude__gt = django_filters.NumberFilter(
        field_name='latitude',
        label=_('Latitude greater than'),
        lookup_expr='gt')
    latitude__lt = django_filters.NumberFilter(
        field_name='latitude',
        label=_('Latitude less than'),
        lookup_expr='lt')

    longitude__gt = django_filters.NumberFilter(
        field_name='longitude',
        label=_('Longitude greater than'),
        lookup_expr='gt')
    longitude__lt = django_filters.NumberFilter(
        field_name='longitude',
        label=_('Longitude less than'),
        lookup_expr='lt')

    altitude__gt = django_filters.NumberFilter(
        field_name='altitude',
        label=_('Altitude less than'),
        lookup_expr='gt')
    altitude__lt = django_filters.NumberFilter(
        field_name='altitude',
        label=_('Altitude less than'),
        lookup_expr='lt')

    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
        )


class Filter(SiteBaseFilter):
    class Meta:
        model = Site
        fields = (
            'created_by',
        )

class UserFilter(SiteBaseFilter):
    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
        )
