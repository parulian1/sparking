from django.db import models

# Create your models here.


class Transaction(models.Model):
    id = models.UUIDField(max_length=15, primary_key=True)
    time_in = models.IntegerField(null=True)
    vehicle = models.ForeignKey('Vehicle', blank=True, null=True, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(default=0, null=True)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_transaction'


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=12)
    type = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transaction_vehicle'