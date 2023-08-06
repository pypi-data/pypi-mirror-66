import django_filters

from irekua_database.models import TermSuggestion


search_fields = (
    'value',
)


class Filter(django_filters.FilterSet):
    created_on__gt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt')
    created_on__lt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt')

    class Meta:
        model = TermSuggestion
        fields = (
            'value',
            'created_by__username',
            'created_by__first_name',
            'created_by__is_superuser',
            'created_by__is_curator'
        )
