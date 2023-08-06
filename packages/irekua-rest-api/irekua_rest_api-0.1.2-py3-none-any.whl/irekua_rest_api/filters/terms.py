from irekua_database.models import Term
from .utils import BaseFilter


search_fields = (
    'value',
)


class Filter(BaseFilter):
    class Meta:
        model = Term
        fields = (
            'value',
        )
