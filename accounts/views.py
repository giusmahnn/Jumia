from django.shortcuts import redirect
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.template.loader import render_to_string
from rest_framework import status

from . utils import *
from .serializers import *
from .models import *
from .permissions import *





class GoogleAuthRedirect(APIView):
    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri=https://adfd-2c0f-f5c0-600-1b0-19d4-83d0-a763-e1cc.ngrok-free.app/google/callback"
        return redirect(redirect_url)



class GoogleRedirect(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"Error": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the authorization code for an access token
        token_uri = "https://oauth2.googleapis.com/token"
        token_params = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri": "https://adfd-2c0f-f5c0-600-1b0-19d4-83d0-a763-e1cc.ngrok-free.app/google/callback",
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_uri, data=token_params)
        if token_response.status_code != 200:
            return Response(
                {"Error": "Failed to fetch access token", "details": token_response.json()},
                status=token_response.status_code
            )

        access_token = token_response.json().get("access_token")
        if not access_token:
            return Response({"Error": "Access token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user profile
        profile_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(profile_endpoint, headers=headers)

        if profile_response.status_code != 200:
            return Response(
                {"Error": "Failed to fetch user profile", "details": profile_response.json()},
                status=profile_response.status_code
            )

        profile_data = profile_response.json()
        data={}
        # Create or update the user account
        user, created = Account.objects.get_or_create(
            email=profile_data["email"],
            defaults={
                "first_name": profile_data.get("given_name", ""),
                "last_name": profile_data.get("family_name", ""),
                "profile_picture": profile_data.get("picture", ""),
            }
        )

        # Update missing fields for existing users
        if not created:
            updated = False
            if not user.first_name and profile_data.get("given_name"):
                user.first_name = profile_data["given_name"]
                updated = True
            if not user.last_name and profile_data.get("family_name"):
                user.last_name = profile_data["family_name"]
                updated = True
            if not user.profile_picture and profile_data.get("picture"):
                user.profile_picture = profile_data["picture"]
                updated = True
            if updated:
                user.save()

        # Prepare response
        serializer = AccountSerializer(user)
        refresh = RefreshToken.for_user(user)

        data["message"] = "User Created Successfully" if created else "User Logged in successfully"
        data["user_details"] = serializer.data
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class VerifyEmail(APIView):
    def get(self, request):
        otp = request.query_params.get("otp")

        if not otp:
            return Response({"message": "Missing OTP"}, status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Account.objects.filter(otp=otp).first()
            user.is_active = True
            user.verification_token = None  # Clear the token after verification
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"Error":"Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)