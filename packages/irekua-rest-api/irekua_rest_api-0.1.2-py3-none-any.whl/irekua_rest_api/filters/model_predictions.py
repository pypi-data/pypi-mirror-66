from irekua_models.models import ModelPrediction
from .utils import BaseFilter


search_fields = (
    'model_version__model__name',
    'model_version__model__annotation_type__name',
    'model_version__version',
    'item__item_type__name',
    'event_type__name',
    'labels__value',
    'labels__term_type__name',
)


class Filter(BaseFilter):
    class Meta:
        model = ModelPrediction
        fields = {
            'item': ['exact'],
            'item__item_type': ['exact'],
            'item__item_type__name': ['exact', 'icontains'],
            'certainty': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'model_version__model': ['exact'],
            'model_version__version': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte'],
            'model_version__model__name': ['exact', 'icontains'],
            'model_version__model__annotation_type': ['exact'],
            'model_version__model__annotation_type__name': ['exact', 'icontains'],
            'event_type': ['exact'],
            'event_type__name': ['exact', 'icontains'],
            'labels': ['exact'],
            'labels__value': ['exact', 'icontains'],
            'labels__term_type': ['exact'],
            'labels__term_type__name': ['exact', 'icontains']
        }
