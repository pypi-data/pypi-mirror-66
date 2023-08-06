from irekua_database.models import DeviceBrand
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = DeviceBrand
        fields = ('name', )
