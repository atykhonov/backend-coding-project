from django.contrib.gis.geos import Polygon
from django.test import TestCase
from djmoney.contrib.exchange.models import ExchangeBackend, Rate
from djmoney.money import Money

from geo.models import Provider, ServiceArea


class GenericTests(TestCase):

    def test_root_has_endpoints_to_explore_api(self):
        response = self.client.get('/api/v1/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('providers', response.data)
        self.assertIn('service-areas', response.data)


class ProviderTests(TestCase):

    def make_provider(self):
        return Provider.objects.create(
            name='example', email='example@example.com',
            phone_number='+41524204242', language='uk'
        )

    def test_get_empty(self):
        response = self.client.get('/api/v1/providers/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data)

    def test_post(self):
        response = self.client.post(
            '/api/v1/providers/',
            {
                'name': 'example',
                'email': 'example@example.com',
                'phone_number': '+41524204242',
                'language': 'uk',
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.data
        self.assertEqual(data['name'], 'example')
        self.assertEqual(data['email'], 'example@example.com')
        self.assertEqual(data['phone_number'], '+41524204242')
        self.assertEqual(data['language'], 'uk')
        self.assertEqual(data['currency'], 'USD')
        self.assertEqual(data['service_areas'], [])

    def test_get_all(self):
        self.make_provider()

        response = self.client.get('/api/v1/providers/')

        self.assertEqual(response.status_code, 200)
        data = response.data[0]
        self.assertEqual(data['name'], 'example')
        self.assertEqual(data['email'], 'example@example.com')
        self.assertEqual(data['phone_number'], '+41524204242')
        self.assertEqual(data['language'], 'uk')
        self.assertEqual(data['currency'], 'USD')
        self.assertEqual(data['service_areas'], [])

    def test_get_single(self):
        provider = self.make_provider()

        response = self.client.get(provider.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'example')
        self.assertEqual(data['email'], 'example@example.com')
        self.assertEqual(data['phone_number'], '+41524204242')
        self.assertEqual(data['language'], 'uk')
        self.assertEqual(data['currency'], 'USD')
        self.assertEqual(data['service_areas'], [])

    def test_put(self):
        provider = self.make_provider()

        response = self.client.put(
            provider.get_absolute_url(),
            {
                'name': 'example1',
                'email': 'example1@example.com',
                'phone_number': '+41524204288',
                'language': 'it',
                'currency': 'CAD',
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'example1')
        self.assertEqual(data['email'], 'example1@example.com')
        self.assertEqual(data['phone_number'], '+41524204288')
        self.assertEqual(data['language'], 'it')
        self.assertEqual(data['currency'], 'CAD')
        self.assertEqual(data['service_areas'], [])

    def test_delete(self):
        provider = self.make_provider()

        self.client.delete(provider.get_absolute_url())

        response = self.client.get('/api/v1/providers/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data)


class ServiceAreaTests(TestCase):

    def setUp(self):
        backend = ExchangeBackend.objects.create(name='test')
        Rate.objects.create(currency='CAD', value=1.5, backend=backend)
        Rate.objects.create(currency='USD', value=1.0, backend=backend)
        self.provider = Provider.objects.create(
            name='example', email='example@example.com',
            phone_number='+41524204242', language='it'
        )
        self.coords = [
            [135.0, 45.0], [140.0, 50.0],
            [145.0, 55.0], [135.0, 45.0],
        ]

    def make_service_area(self, coords=None):
        coords = coords or self.coords
        return ServiceArea.objects.create(
            provider=self.provider, name='area1', price=Money(10, 'USD'),
            area=str(Polygon(coords))
        )

    def test_get_empty(self):
        response = self.client.get('/api/v1/service-areas/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data)

    def test_post(self):
        response = self.client.post(
            '/api/v1/service-areas/',
            {
                'provider': self.provider.id,
                'name': 'area1',
                'area': str(Polygon(self.coords)),
                'price': 20,
                'price_currency': 'USD',
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.data
        self.assertEqual(data['provider'], self.provider.get_absolute_url())
        self.assertEqual(data['name'], 'area1')
        self.assertEqual(data['price'], 20.00)
        self.assertEqual(data['price_currency'], 'USD')
        geo_json_dict = data['area']
        self.assertEqual(geo_json_dict['type'], 'Polygon')
        self.assertEqual(geo_json_dict['coordinates'][0], self.coords)

    def test_get_all(self):
        self.make_service_area()

        response = self.client.get('/api/v1/service-areas/')

        self.assertEqual(response.status_code, 200)
        data = response.data[0]
        self.assertEqual(data['name'], 'area1')
        self.assertEqual(data['provider'], self.provider.get_absolute_url())
        geo_json_dict = data['area']
        self.assertEqual(geo_json_dict['type'], 'Polygon')
        self.assertEqual(geo_json_dict['coordinates'][0], self.coords)

    def test_get_single(self):
        service_area = self.make_service_area()

        response = self.client.get(service_area.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'area1')
        self.assertEqual(data['provider'], self.provider.get_absolute_url())
        geo_json_dict = data['area']
        self.assertEqual(geo_json_dict['type'], 'Polygon')
        self.assertEqual(geo_json_dict['coordinates'][0], self.coords)

    def test_put(self):
        service_area = self.make_service_area()

        coords = self.coords[:]
        coords[0][0] = 115.0
        coords[0][1] = 25.0
        coords[3][0] = 115.0
        coords[3][1] = 25.0
        response = self.client.put(
            service_area.get_absolute_url(),
            {
                'provider': self.provider.id,
                'name': 'area2',
                'area': str(Polygon(coords)),
                'price': 30.00,
                'price_currency': 'USD',
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'area2')
        self.assertEqual(data['price'], 30.00)
        self.assertEqual(data['price_currency'], 'USD')
        geo_json_dict = data['area']
        self.assertEqual(geo_json_dict['type'], 'Polygon')
        self.assertEqual(geo_json_dict['coordinates'][0], coords)

    def test_delete(self):
        service_area = self.make_service_area()

        self.client.delete(service_area.get_absolute_url())

        response = self.client.get('/api/v1/service-areas/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data)

    def test_area_list_in_provider(self):
        service_area = self.make_service_area()

        response = self.client.get(self.provider.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            service_area.get_absolute_url(), response.data['service_areas'][0])

    def test_get_empty_by_provider_id(self):
        self.make_service_area()
        provider2 = Provider.objects.create(
            name='example2', email='example2@example.com',
            phone_number='+41524202222', language='en'
        )

        response = self.client.get(
            '/api/v1/service-areas/?provider_id={}'.format(provider2.id))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data)

    def test_get_single_by_provider_id(self):
        service_area = self.make_service_area()

        response = self.client.get(
            '/api/v1/service-areas/?provider_id={}'.format(self.provider.id))

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data[0]['id'], service_area.id)
        self.assertEqual(data[0]['name'], service_area.name)

    def test_get_empty_by_lat_lng(self):
        coords = [
            [10.0, 10.0], [10.0, 50.0],
            [50.0, 50.0], [50.0, 10.0],
            [10.0, 10.0],
        ]
        self.make_service_area(coords=coords)

        response = self.client.get('/api/v1/service-areas/?lat=5.0&lng=5.0')

        self.assertEqual(response.data, [])

    def test_get_single_by_lat_lng(self):
        coords = [
            [10.0, 10.0], [10.0, 50.0],
            [50.0, 50.0], [50.0, 10.0],
            [10.0, 10.0],
        ]
        service_area = self.make_service_area(coords=coords)

        response = self.client.get('/api/v1/service-areas/?lat=15.0&lng=15.0')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], service_area.id)

    def test_get_intersected_by_lat_lng(self):
        coords1 = [
            [10.0, 10.0], [10.0, 50.0],
            [50.0, 50.0], [50.0, 10.0],
            [10.0, 10.0],
        ]
        coords2 = [
            [40.0, 40.0], [40.0, 90.0],
            [90.0, 90.0], [90.0, 40.0],
            [40.0, 40.0],
        ]
        service_area1 = self.make_service_area(coords=coords1)
        service_area2 = self.make_service_area(coords=coords2)

        response = self.client.get('/api/v1/service-areas/?lat=45.0&lng=45.0')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], service_area1.id)
        self.assertEqual(response.data[1]['id'], service_area2.id)

    def test_default_price_and_currency(self):
        service_area = self.make_service_area()

        response = self.client.get(service_area.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['price'], 10.00)
        self.assertEqual(response.data['price_currency'], 'USD')

    def test_changed_price_when_currency_is_changed(self):
        service_area = self.make_service_area()
        response = self.client.put(
            self.provider.get_absolute_url(),
            {
                'name': 'example',
                'email': 'example@example.com',
                'phone_number': '+41524204288',
                'language': 'it',
                'currency': 'CAD',
            },
            content_type='application/json'
        )

        response = self.client.get(service_area.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['price'], 15.00)
        self.assertEqual(response.data['price_currency'], 'CAD')
