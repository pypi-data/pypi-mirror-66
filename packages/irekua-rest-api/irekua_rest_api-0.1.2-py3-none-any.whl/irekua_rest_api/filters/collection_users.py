from irekua_database.models import CollectionUser
from .utils import BaseFilter


search_fields = (
    'user__username',
    'user__first_name',
    'user__last_name',
)


class Filter(BaseFilter):
    class Meta:
        model = CollectionUser
        fields = (
            'user__username',
            'user__first_name',
            'user__last_name',
            'user__institution__institution_name',
            'user__institution__institution_code',
            'user__institution__subdependency',
            'user__is_superuser',
            'user__is_curator',
            'user__is_model',
            'user__is_developer',
            'role',
        )
