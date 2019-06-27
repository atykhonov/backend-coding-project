from geo.models import Provider, ServiceArea
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer


class ServiceAreaSerializer(GeoModelSerializer):
    provider = serializers.HyperlinkedRelatedField(
        queryset=Provider.objects.all(), lookup_field='pk',
        view_name='v1:provider-detail'
    )

    class Meta:
        model = ServiceArea
        geo_field = 'area'
        fields = ('id', 'provider', 'name', 'area')


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    service_areas = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='v1:serviceareas-detail',
    )

    class Meta:
        model = Provider
        fields = (
            'id', 'name', 'email', 'phone_number', 'language', 'service_areas')
