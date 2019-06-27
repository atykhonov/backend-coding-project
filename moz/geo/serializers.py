from geo.models import Provider, ServiceArea
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer


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


class ServiceAreaSerializer(GeoModelSerializer):

    class Meta:
        model = ServiceArea
        geo_field = 'area'
        fields = ('id', 'provider', 'name', 'area')

    def to_representation(self, instance):
        representation = super(
            ServiceAreaSerializer, self).to_representation(instance)
        representation['provider'] = '/api/v1/providers/{}/'.format(
            instance.provider.id)
        return representation
