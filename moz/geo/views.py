from geo.models import Provider, ServiceArea
from geo.serializers import ProviderSerializer, ServiceAreaSerializer
from rest_framework import viewsets


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows service areas to be viewed or edited.
    """

    serializer_class = ServiceAreaSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned service areas to a given
        provider, latitute and longitude by filtering against a
        `provider_id`, `lat` and `lng` query parameters in the URL
        respectively.
        """
        params = self.request.query_params
        queryset = ServiceArea.objects.all()
        provider_id = params.get('provider_id', None)
        if provider_id is not None:
            queryset = queryset.filter(provider__id=provider_id)
        lat = params.get('lat', None)
        lng = params.get('lng', None)
        if lat and lng:
            queryset = queryset.filter(
                area__contains='POINT({} {})'.format(lat, lng))
        return queryset
