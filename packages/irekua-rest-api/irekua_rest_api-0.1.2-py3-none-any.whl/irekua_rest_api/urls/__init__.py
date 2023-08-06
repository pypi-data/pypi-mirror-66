from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url('v1/', include(('irekua_rest_api.urls.api', 'irekua_rest_api'), namespace='v1')),
    url('docs/', include_docs_urls(title='Irekua REST API documentation')),
    url('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
