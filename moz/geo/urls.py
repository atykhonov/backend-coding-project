from django.urls import include, path
from rest_framework import routers

from geo import views


router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(
    r'service-areas', views.ServiceAreaViewSet, base_name='serviceareas')

urlpatterns = [
    path('', include(router.urls)),
]
