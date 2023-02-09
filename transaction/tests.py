import datetime
import random

from django.test import TestCase
import json
from http import HTTPStatus

from django.test import TestCase
import factory
from factory import fuzzy

from rest_framework.test import APILiveServerTestCase

from transaction.models import Vehicle, Transaction


# Create your tests here.
class VehicleFactory(factory.django.DjangoModelFactory):
    license_plate = fuzzy.FuzzyText(length=12)
    type = 'small'

    class Meta:
        model = Vehicle


class TransactionFactory(factory.django.DjangoModelFactory):
    id = factory.Faker('uuid4')
    time_in = int(datetime.datetime.now().timestamp())
    vehicle = factory.SubFactory(VehicleFactory)

    class Meta:
        model = Transaction


class TransactionPayTests(APILiveServerTestCase):
    def setup(self):
        pass

    def test_pay(self):
        with self.subTest('Successfully pay transaction'):
            transaction = TransactionFactory()
            now = datetime.datetime.now()
            later = now + datetime.timedelta(hours=random.randint(0, 24), minutes=random.randint(1, 59))
            create_resp = self.client.post(
                f'/api/transaction/{transaction.id}/pay/',
                data=json.dumps({
                    'license_plate': transaction.vehicle.license_plate,
                    'time_in': int(later.timestamp())
                }),
                content_type='application/json'
            )
            self.assertEqual(create_resp.status_code, HTTPStatus.OK)

        with self.subTest('Failed pay transaction - invalid license plate'):
            transaction = TransactionFactory()
            now = datetime.datetime.now()
            later = now + datetime.timedelta(hours=random.randint(0, 24), minutes=random.randint(1, 59))
            create_resp = self.client.post(
                f'/api/transaction/{transaction.id}/pay/',
                data=json.dumps({
                    'license_plate': 'B 3 JO',
                    'time_in': int(later.timestamp())
                }),
                content_type='application/json'
            )
            self.assertEqual(create_resp.status_code, HTTPStatus.BAD_REQUEST)

        with self.subTest('Failed pay transaction - invalid time in'):
            transaction = TransactionFactory()
            now = datetime.datetime.now()
            later = now - datetime.timedelta(hours=random.randint(0, 24), minutes=random.randint(1, 59))
            create_resp = self.client.post(
                f'/api/transaction/{transaction.id}/pay/',
                data=json.dumps({
                    'license_plate': transaction.vehicle.license_plate,
                    'time_in': 1231233
                }),
                content_type='application/json'
            )
            self.assertEqual(create_resp.status_code, HTTPStatus.BAD_REQUEST)

