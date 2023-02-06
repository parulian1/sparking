from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from transaction.models import Transaction
from transaction.serializers import TransactionPaySerializer, TransactionResponseSerializer


# Create your views here.
class TransactionPayView(generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionPaySerializer
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        create_serializer = self.get_serializer(instance, data=request.data)
        create_serializer.is_valid(raise_exception=True)
        self.perform_update(create_serializer)
        headers = self.get_success_headers(create_serializer.data)
        response_serializer = TransactionResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer['is_paid'] = True
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}




