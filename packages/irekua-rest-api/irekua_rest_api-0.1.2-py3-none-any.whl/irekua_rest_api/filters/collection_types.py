from irekua_database.models import CollectionType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = CollectionType
        fields = (
            'name',
            'anyone_can_create',
        )
