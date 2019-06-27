from django.contrib.gis.db import models as models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from languages.fields import LanguageField
from phonenumber_field.modelfields import PhoneNumberField


US_DOLLAR = 'USD'
EURO = 'EUR'
CANADIAN_DOLLAR = 'CAD'


class Provider(models.Model):
    CURRENCIES = [
        (US_DOLLAR, 'USD'),
        (EURO, 'EUR'),
        (CANADIAN_DOLLAR, 'CAD'),
    ]
    name = models.CharField(null=False, blank=False, max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    language = LanguageField()
    currency = models.CharField(
        null=False, blank=False, max_length=3, choices=CURRENCIES,
        default=US_DOLLAR
    )

    def get_absolute_url(self):
        return reverse('v1:providers-detail', args=[str(self.id)])


class ServiceArea(models.Model):
    provider = models.ForeignKey(
        Provider, related_name='service_areas', on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=100)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency=US_DOLLAR)
    area = models.PolygonField()

    def get_absolute_url(self):
        return reverse('v1:serviceareas-detail', args=[str(self.id)])
