from rest_framework.permissions import IsAuthenticated

from .generic import IsUnauthenticated
from .generic import IsDeveloper
from .generic import IsModel
from .generic import IsCurator
from .generic import IsAdmin
from .generic import ReadOnly
from .generic import IsSpecialUser


__all__ = [
    'IsUnauthenticated',
    'IsDeveloper',
    'IsModel',
    'IsCurator',
    'IsAdmin',
    'IsSpecialUser',
    'IsAuthenticated',
    'ReadOnly',
]
