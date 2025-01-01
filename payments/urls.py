from django.urls import path
from.views import *



urlpatterns = [
    # path("paystack/callback/", PaystackCallbackView.as_view(), name="paystack-callback"),
    path("paystack/initiate/", InitiatePaymentView.as_view(), name="paystack-initiate"),
    path("paystack/webhook/", PaystackWebhookView.as_view())
]