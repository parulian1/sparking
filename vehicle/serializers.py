from rest_framework import serializers

from vehicle.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            'license_plate',
            'type',
        )
