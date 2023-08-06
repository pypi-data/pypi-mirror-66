from irekua_database.models import Entailment
from .utils import BaseFilter


search_fields = (
    'source__value',
    'source__term_type__name',
    'target__value',
    'target__term_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = Entailment
        fields = (
            'source__value',
            'source__term_type__name',
            'target__value',
            'target__term_type__name',
        )
