from django.contrib.gis.db import models as models
from django.urls import reverse
from languages.fields import LanguageField
from phonenumber_field.modelfields import PhoneNumberField


class Provider(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    language = LanguageField()

    def get_absolute_url(self):
        return reverse('v1:providers-detail', args=[str(self.id)])


class ServiceArea(models.Model):
    provider = models.ForeignKey(
        Provider, related_name='service_areas', on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=100)
    area = models.PolygonField()

    def get_absolute_url(self):
        return reverse('v1:serviceareas-detail', args=[str(self.id)])
