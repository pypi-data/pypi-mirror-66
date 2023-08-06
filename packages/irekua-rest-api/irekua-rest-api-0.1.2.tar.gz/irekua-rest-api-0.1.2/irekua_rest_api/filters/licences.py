from django import forms
import django_filters

from irekua_database.models import Licence

search_fields = (
    'licence_type',
)


class Filter(django_filters.FilterSet):
    created_on__lt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='lt',
        widget=forms.DateTimeInput)
    created_on__gt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt',
        widget=forms.DateTimeInput)

    class Meta:
        model = Licence
        fields = (
            'licence_type',
            'is_active',
            'created_by__username',
            'created_by__first_name',
            'created_by__last_name',
            'licence_type__years_valid_for',
            'licence_type__can_view',
            'licence_type__can_download',
            'licence_type__can_view_annotations',
            'licence_type__can_annotate',
            'licence_type__can_vote_annotations',
        )
