import datetime

from rest_framework import serializers, exceptions

from transaction.models import Transaction, Vehicle


class TransactionPaySerializer(serializers.Serializer):
    license_plate = serializers.CharField(max_length=12)
    time_in = serializers.IntegerField()

    def validate_license_plate(self, license_plate: str):
        not_exists = not Vehicle.objects.filter(license_plate__iexact=license_plate).exists()
        if not_exists:
            raise serializers.ValidationError('Invalid license plate')
        return license_plate

    def validate_time_in(self, time_in_value: int):
        now = datetime.datetime.now()
        time_in = datetime.datetime.fromtimestamp(time_in_value)
        if time_in <= now:
            raise serializers.ValidationError('Invalid time in')
        return time_in_value


class TransactionResponseSerializer(serializers.ModelSerializer):
    time_in = serializers.SerializerMethodField()
    license_plate = serializers.SerializerMethodField()

    def get_time_in(self, obj: Transaction):
        return datetime.datetime.fromtimestamp(obj.time_in/1000).strftime('%y-%m-%d %h:%m:%s')

    def get_license_plate(self, obj: Transaction):
        return obj.vehicle.license_plate

    class Meta:
        model = Transaction
        fields = (
            'id',
            'amount',
            'time_in',
            'license_plate'
        )
