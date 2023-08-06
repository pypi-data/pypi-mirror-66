from irekua_database.models import Institution
from .utils import BaseFilter


search_fields = (
    'institution_name',
    'institution_code',
)


class Filter(BaseFilter):
    class Meta:
        model = Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country'
        )
