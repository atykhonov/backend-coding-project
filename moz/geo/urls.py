from django.urls import include, path
from rest_framework import routers

from geo import views


router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet, basename='providers')
router.register(
    r'service-areas', views.ServiceAreaViewSet, basename='serviceareas')

urlpatterns = [
    path('v1/', include((router.urls, 'api_v1'), namespace='v1')),
]
