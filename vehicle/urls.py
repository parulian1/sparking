from django.urls import path

from vehicle.views import VehicleView

urlpatterns = [
    path('', VehicleView.as_view(), name='vehicle-registration'),
]