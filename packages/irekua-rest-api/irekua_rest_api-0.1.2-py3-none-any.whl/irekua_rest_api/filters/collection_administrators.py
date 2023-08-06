from irekua_database.models import Collection
from django_filters import FilterSet


search_fields = (
    'user__username',
    'user__first_name',
    'user__last_name',
)


class Filter(FilterSet):
    class Meta:
        model = Collection.administrators.through
        fields = (
            'user__username',
            'user__first_name',
            'user__last_name',
        )
