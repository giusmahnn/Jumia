import json
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from orders.models import Order
from payments.models import Payment


# Create your views here.


class InitiatePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        order = get_object_or_404(Order, id=order_id, customer=request.user)
        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        if not amount or amount < 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        
        headers = {
            'Authorization': f'Bearer {settings.TEST_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "email": request.user.email,
            "amount": amount,
            "reference": f"PAY-{request.user.id}-{order.id}",
            "callback_url": "https://609d-2c0f-f5c0-719-53a3-809f-2649-fca2-2e45.ngrok-free.app/paystack/callback/",
        }

        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            Payment.objects.create(
                user=request.user,
                order=order,
                amount=amount,
                gateway_response=response.json(),
                refererence = data["reference"],
                status=Payment.status.pending
                )
            return Response({"authorization_url": data["data"]["authorization_url"]}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to initialize payment with Paystack."}, status=status.HTTP_400_BAD_REQUEST)
