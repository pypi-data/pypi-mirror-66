from django.conf.urls import url, include
from irekua_rest_api.urls.main import main_router


urlpatterns = [
    url(r'^', include(main_router.urls)),
]
