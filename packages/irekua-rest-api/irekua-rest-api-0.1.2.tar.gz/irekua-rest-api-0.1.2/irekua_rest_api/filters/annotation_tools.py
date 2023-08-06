from irekua_database.models import AnnotationTool
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = AnnotationTool
        fields = (
            'name',
            'version')
