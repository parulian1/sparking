import json
from typing import Type

from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Vehicle(models.Model):
    class MotorcycleType(models.TextChoices):
        SCOOTERS = 'scooters', 'Skutik/bebek'
        MEDIUM_BIKE = 'medium', 'Dibawah 500cc'
        BIG_BIKE = 'big', 'Diatas 500cc'
        ELECTRIC = 'electric', 'elektrik'
    license_plate = models.CharField(max_length=12)
    type = models.CharField(max_length=10, choices=MotorcycleType.choices, default=MotorcycleType.SCOOTERS)
    created = models.DateTimeField(_('created'), auto_now_add=True, help_text=_('Date/time this object was created.'))
    modified = models.DateTimeField(_('modified'), auto_now=True,
                                    help_text=_('Date/time this object was last updated.'))

    class Meta:
        db_table = 'vehicle_vehicle'


@receiver(models.signals.post_save, sender=Vehicle)
def send_vehicle_information(sender: Type[Vehicle], instance: Vehicle, created: bool, **kwargs):
    import pika

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='vehicle')

    from vehicle.serializers import VehicleSerializer
    channel.basic_publish(exchange='', routing_key='vehicle', body=json.dumps(VehicleSerializer(instance).data))
    connection.close()