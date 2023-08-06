from irekua_database.models import EventType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = EventType
        fields = ('name', )
