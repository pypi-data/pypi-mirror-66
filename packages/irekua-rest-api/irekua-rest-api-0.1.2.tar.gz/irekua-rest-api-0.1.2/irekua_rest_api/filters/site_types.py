from irekua_database.models import SiteType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = SiteType
        fields = ('name', )
