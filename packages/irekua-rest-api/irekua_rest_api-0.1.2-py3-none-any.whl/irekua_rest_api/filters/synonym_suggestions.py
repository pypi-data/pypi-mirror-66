import django_filters

from irekua_database.models import SynonymSuggestion


search_fields = (
    'source__value',
    'synonym',
)


class Filter(django_filters.FilterSet):
    created_on__gt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt')
    created_on__lt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt')

    class Meta:
        model = SynonymSuggestion
        fields = (
            'source__value',
            'synonym',
            'created_by__username',
            'created_by__first_name',
        )
