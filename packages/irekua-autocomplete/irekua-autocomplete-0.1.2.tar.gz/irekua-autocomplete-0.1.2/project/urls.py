from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(r'^autocomplete/', include('irekua_autocomplete.urls')),
]
