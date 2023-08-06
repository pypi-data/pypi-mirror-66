from irekua_database.models import Synonym
from .utils import BaseFilter


search_fields = (
    'source__value',
    'target__value',
)


class Filter(BaseFilter):
    class Meta:
        model = Synonym
        fields = (
            'source__value',
            'target__value'
        )
