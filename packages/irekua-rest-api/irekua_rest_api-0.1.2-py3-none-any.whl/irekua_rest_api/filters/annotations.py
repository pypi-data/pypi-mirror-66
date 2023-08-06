from irekua_database.models import Annotation
from .utils import BaseFilter


search_fields = (
    'annotation_type__name',
    'event_type__name',
    'created_by__username',
)


class Filter(BaseFilter):
    class Meta:
        model = Annotation
        fields = (
            'annotation_type__name',
            'annotation_tool__name',
            'event_type__name',
            'quality',
            'created_by__username',
            'modified_by__username',
        )
