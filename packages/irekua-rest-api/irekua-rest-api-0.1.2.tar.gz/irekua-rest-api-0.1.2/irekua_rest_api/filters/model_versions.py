from django import forms
import django_filters

from irekua_database.models import Term
from irekua_models.models import ModelVersion
from .utils import BaseFilter


search_fields = (
    'version',
    'model__name',
    'model__annotation_type__name',
    'model__event_types__name',
    'model__terms__value',
)


class Filter(BaseFilter):
    terms = django_filters.ModelMultipleChoiceFilter(
        field_name='model__terms',
        queryset=Term.objects.all(),
        widget=forms.TextInput)

    class Meta:
        model = ModelVersion
        fields = {
            'version': ['exact', 'icontains', 'lt', 'gt', 'lte', 'gte'],
            'model': ['exact'],
            'model__name': ['exact', 'icontains'],
            'model__annotation_type': ['exact'],
            'model__annotation_type__name': ['exact', 'icontains'],
            'model__event_types': ['exact'],
            'model__event_types__name': ['exact', 'icontains'],
            'model__terms__value': ['exact', 'icontains']
        }
