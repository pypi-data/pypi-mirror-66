from irekua_database.models import AnnotationVote
from .utils import BaseFilter


search_fields = (
    'created_by__username',
)


class Filter(BaseFilter):
    class Meta:
        model = AnnotationVote
        fields = (
            'created_by__username',
            'created_by__first_name',
            'created_by__last_name',
        )
