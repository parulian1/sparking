from rest_framework import generics
from rest_framework.permissions import AllowAny

from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer


# Create your views here.
class VehicleView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny,]