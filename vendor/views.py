from django.shortcuts import render
from rest_framework.response import Response
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from accounts.utils import *
from accounts.models import *
from rest_framework.views import APIView
# Create your views here.



class VendorCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        url = "https://adfd-2c0f-f5c0-600-1b0-19d4-83d0-a763-e1cc.ngrok-free.app"
        
        # Validate the serializer
        if serializer.is_valid():
            user = serializer.save()
            user.save()

            # Prepare email context
            context = {
                "name": user.user.first_name,
                "verify_link": f"{url}/verify-email/?otp={user.user.otp}",
                "subject": "Verify your Jumia account"
            }

            # Render email template and send email
            template = render_to_string("accounts/verify-email.html", context)
            send_email(user.user.email, "Verify Your Account", template)

            # Prepare response data
            data = {
                "Message": "Account Created Successfully",
                "Vendor_info": VendorSerializer(user).data,
                "Token": jwt_auth(user)
            }

            return Response(data, status=status.HTTP_201_CREATED)
        
        # Handle validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VendorLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VendorLoginSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            vendor_user = serializer.validated_data['user']  # Get the Account instance
            vendor = vendor_user.vendor # Get the Vendor instance through the Vendor instance attribute related
            data = {
                "Vendor_info": VendorSerializer(vendor).data,
                "Token": jwt_auth(vendor_user)
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


