from django import forms
import django_filters

from irekua_database.models import Term
from irekua_models.models import Model
from .utils import BaseFilter


search_fields = (
    'name',
    'annotation_type__name',
    'event_types__name',
    'terms__value',
)


class Filter(BaseFilter):
    terms = django_filters.ModelMultipleChoiceFilter(
        queryset=Term.objects.all(),
        widget=forms.TextInput)

    class Meta:
        model = Model
        fields = {
            'name': ['exact', 'icontains'],
            'annotation_type': ['exact'],
            'annotation_type__name': ['exact', 'icontains'],
            'event_types': ['exact'],
            'event_types__name': ['exact', 'icontains'],
            'terms__value': ['exact', 'icontains']
        }
