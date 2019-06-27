from django.urls import include, path
from rest_framework import routers

from geo import views


router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(
    r'service-areas', views.ServiceAreaViewSet, base_name='serviceareas')

urlpatterns = [
    path('v1/', include((router.urls, 'api_v1'), namespace='v1')),
]
