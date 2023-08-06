from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(r'^api/', include('irekua_rest_api.urls')),
]
