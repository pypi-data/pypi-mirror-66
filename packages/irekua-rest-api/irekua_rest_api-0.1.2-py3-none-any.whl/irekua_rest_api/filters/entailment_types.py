from irekua_database.models import EntailmentType
from .utils import BaseFilter


search_fields = (
    'source_type__name',
    'target_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = EntailmentType
        fields = (
            'source_type__name',
            'target_type__name',
        )
