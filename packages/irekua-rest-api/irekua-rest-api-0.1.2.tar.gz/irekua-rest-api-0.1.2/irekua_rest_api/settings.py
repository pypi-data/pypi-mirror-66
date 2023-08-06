IREKUA_REST_API_APPS = [
    'irekua_rest_api',
    'rest_framework',
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'irekua_rest_api.pagination.StandardResultsSetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_METADATA_CLASS': 'irekua_rest_api.metadata.CustomMetadata',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'irekua_rest_api.exception_handler.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'irekua_rest_api.utils.schemas.CustomSchema'
}
