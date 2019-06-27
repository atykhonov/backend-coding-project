from geo.models import Provider
from rest_framework import serializers


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language')
