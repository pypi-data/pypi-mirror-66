from irekua_database.models import MetaCollection
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = MetaCollection
        fields = (
            'name',
        )
