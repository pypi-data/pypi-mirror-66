from irekua_database.models import Tag
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = Tag
        fields = (
            'name',
        )
