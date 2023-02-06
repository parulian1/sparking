import json
from http import HTTPStatus

from django.test import TestCase
import factory
from factory import fuzzy

from rest_framework.test import APILiveServerTestCase

from vehicle.models import Vehicle


# Create your tests here.
class VehicleFactory(factory.django.DjangoModelFactory):
    license_plate = factory.Faker('name')
    type = fuzzy.FuzzyChoice([x[0] for x in Vehicle.MotorcycleType])

    class Meta:
        model = Vehicle


class VehicleTests(APILiveServerTestCase):
    def setup(self):
        pass

    def test_register(self):
        with self.subTest('Successfully register vehicle'):
            create_resp = self.client.post(
                '/api/vehicle/',
                data=json.dumps({
                    'license_plate': 'B 3096 BFF',
                    'type': 'medium'
                }),
                content_type='application/json'
            )
            self.assertEqual(create_resp.status_code, HTTPStatus.CREATED)

        with self.subTest('Cannot do other method beside POST'):
            put_resp = self.client.put(
                '/api/vehicle/',
                data=json.dumps({
                    'license_plate': 'B 3096 BFF',
                    'type': 'medium'
                }),
                content_type='application/json'
            )
            self.assertNotEqual(put_resp.status_code, HTTPStatus.CREATED)

            get_resp = self.client.get(
                '/api/vehicle/',
            )
            self.assertNotEqual(get_resp.status_code, HTTPStatus.CREATED)