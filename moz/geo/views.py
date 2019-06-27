from geo.models import Provider
from geo.serializers import ProviderSerializer
from rest_framework import viewsets


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
