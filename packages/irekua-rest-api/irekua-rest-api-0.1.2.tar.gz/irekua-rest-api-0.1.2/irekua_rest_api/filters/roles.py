from irekua_database.models import Role
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = Role
        fields = (
            'name',
        )
