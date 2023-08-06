from irekua_database.models import ItemType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = ItemType
        fields = (
            'name',
        )
