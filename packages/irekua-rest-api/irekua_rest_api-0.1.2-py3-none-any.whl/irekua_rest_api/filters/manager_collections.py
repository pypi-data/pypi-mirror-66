from irekua_database.models import Collection
from .utils import BaseFilter


search_fields = (
    'name',
    'collection_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = Collection
        fields = (
            'name',
            'collection_type__name',
            'institution__institution_code',
            'institution__institution_name',
            'institution__country',
        )
