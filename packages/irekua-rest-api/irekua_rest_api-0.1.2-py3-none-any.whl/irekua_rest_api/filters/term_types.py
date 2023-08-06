from irekua_database.models import TermType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = TermType
        fields = ('name', )
