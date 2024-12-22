from django.urls import path
from.views import *



urlpatterns = [
    path("paystack/callback/", InitiatePaymentView.as_view())
]