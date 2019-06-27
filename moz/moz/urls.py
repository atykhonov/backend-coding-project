from django.conf.urls import include, url
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'api/', include('geo.urls')),
    url(r'^.*$', RedirectView.as_view(
        url='/api/v1', permanent=False), name='index')
]
