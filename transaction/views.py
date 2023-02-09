import datetime
import math

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from transaction.models import Transaction, Vehicle
from transaction.serializers import TransactionPaySerializer, TransactionResponseSerializer


# Create your views here.
class TransactionPayView(generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionPaySerializer
    lookup_field = 'id'
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        self.perform_update(create_serializer, instance)
        headers = self.get_success_headers(create_serializer.data)
        response_serializer = TransactionResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_update(self, serializer, instance: Transaction):
        instance.vehicle = Vehicle.objects.filter(
            license_plate__iexact=serializer.validated_data.get('license_plate')
        ).first()
        if not instance.is_paid:
            instance.is_paid = True
            instance.amount = self.get_paid_amount(
                instance=instance,
            )
        instance.save()

    def get_paid_amount(self, instance):
        conv_time_in = datetime.datetime.fromtimestamp(instance.time_in).replace(tzinfo=None)
        total_hours = math.ceil((conv_time_in - instance.created.replace(tzinfo=None)).total_seconds() / (60 * 60))
        return total_hours * 2_000

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}




