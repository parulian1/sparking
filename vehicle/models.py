from django.db import models
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
