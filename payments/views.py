import json
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from orders.models import Order
from .models import Payment
from .choices import Status


# class InitiatePaymentView(APIView):
#     def post(self, request):
#         order_id = request.data.get('order_id')
#         amount = request.data.get('amount')

#         print(f"Received order_id: {order_id}, amount: {amount}")

#         order = get_object_or_404(Order, id=order_id, customer=request.user)
#         if not order:
#             print("Order not found")
#             return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
#         if not amount or amount < 0:
#             print("Invalid amount")
#             return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        
#         headers = {
#             'Authorization': f'Bearer {settings.TEST_SECRET_KEY}',
#             'Content-Type': 'application/json'
#         }

#         data = {
#             "email": request.user.email,
#             "amount": int(amount * 100),
#             "reference": Payment.generate_reference(),
#             "callback_url": 'https://2a54-2c0f-f5c0-713-db11-4cd-6ee6-f72f-25a4.ngrok-free.app/paystack/callback/',
#         }

#         print(f"Sending request to Paystack with data: {data}")

#         response = requests.post(
#             'https://api.paystack.co/transaction/initialize',
#             headers=headers,
#             data=json.dumps(data)
#         )
#         print(f"Received response from Paystack: {response.status_code} - {response.text}")

#         if response.status_code == 200:
#             response_data = response.json()
#             Payment.objects.create(
#                 user=request.user,
#                 order=order,
#                 amount=amount,
#                 gateway_response=response_data,
#                 reference=data["reference"],
#                 status=Status.PENDING
#             )
#             print("Payment initialized successfully")
#             return Response({"authorization_url": response_data["data"]["authorization_url"]}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Failed to initialize payment with Paystack."}, status=status.HTTP_400_BAD_REQUEST)



class InitiatePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        print(f"Received order_id: {order_id}, amount: {amount}")

        order = get_object_or_404(Order, id=order_id, customer=request.user)
        if not order:
            print("Order not found")
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        if not amount or amount < 0:
            print("Invalid amount")
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        
        headers = {
            'Authorization': f'Bearer {settings.TEST_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        
        payment = Payment(
            user=request.user,
            order=order,
            amount=amount,
            status=Status.PENDING
        )
        payment.reference = payment.generate_reference()

        data = {
            "email": request.user.email,
            "amount": int(amount * 100),  
            "reference": payment.reference,
            "callback_url": request.build_absolute_uri('/paystack/callback/'),
        }

        print(f"Sending request to Paystack with data: {data}")
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers=headers,
            data=json.dumps(data)
        )
        print(f"Received response from Paystack: {response.status_code} - {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            payment.gateway_response = response_data
            payment.save()
            print("Payment initialized successfully")
            return Response({"authorization_url": response_data["data"]["authorization_url"]}, status=status.HTTP_200_OK)
        else:
            print("Failed to initialize payment with Paystack")
            return Response({"error": "Failed to initialize payment with Paystack."}, status=status.HTTP_400_BAD_REQUEST)




class PaystackCallbackView(APIView):
    def get(self, request):
        reference = request.query_params.get('reference')
        payment = get_object_or_404(Payment, reference=reference)

        headers = {
            'Authorization': f'Bearer {settings.TEST_SECRET_KEY}',
        }

        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers
        )

        if response.status_code == 200:
            response_data = response.json()
            if response_data['data']['status'] == 'success':
                payment.status = Status.SUCCESSFUL
                payment.save()
                return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
            else:
                payment.status = Status.FAILED
                payment.save()
                return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Failed to verify payment with Paystack."}, status=status.HTTP_400_BAD_REQUEST)