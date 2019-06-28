from djmoney.contrib.exchange.models import convert_money
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
            'id', 'name', 'email', 'phone_number', 'language', 'currency',
            'service_areas'
        )


class ServiceAreaSerializer(GeoModelSerializer):
    price_currency = serializers.CharField(
        read_only=True, source="provider.currency")

    class Meta:
        model = ServiceArea
        geo_field = 'area'
        fields = ('id', 'provider', 'name', 'price', 'price_currency', 'area')

    def to_representation(self, instance):
        representation = super(
            ServiceAreaSerializer, self).to_representation(instance)
        representation['provider'] = '/api/v1/providers/{}/'.format(
            instance.provider.id)
        representation['price'] = convert_money(
            instance.price, instance.provider.currency).amount
        return representation
