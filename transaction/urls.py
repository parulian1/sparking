from django.urls import path

from transaction.views import TransactionPayView

urlpatterns = [
    path('<id>/pay/', TransactionPayView.as_view(), name='transaction-pay'),
]