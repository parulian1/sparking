import datetime

from rest_framework import serializers

from transaction.models import Transaction, Vehicle


class TransactionPaySerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(max_length=12)

    def validate_license_plate(self, license_plate: str):
        not_exists = not Vehicle.objects.filter(license_plate__iexact=license_plate).exists()
        if not_exists:
            return serializers.ValidationError('Invalid license plate')
        return license_plate

    class Meta:
        model = Transaction
        fields = (
            'license_plate',
            'time_in',
        )


class TransactionResponseSerializer(serializers.ModelSerializer):
    time_in = serializers.SerializerMethodField()

    def get_time_in(self, obj: Transaction):
        return datetime.datetime.fromtimestamp(obj.time_in/1000).strftime('%y-%m-%d %h:%m:%s')

    class Meta:
        model = Transaction
        fields = (
            'id',
            'amount',
            'time_in',
            'license_plate'
        )
