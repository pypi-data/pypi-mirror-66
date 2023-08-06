from irekua_database.models import SecondaryItem
from .utils import BaseFilter


search_fields = (
    'item_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = SecondaryItem
        fields = (
            'item_type__name',
        )
