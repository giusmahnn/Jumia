from django.shortcuts import redirect
from django.conf import settings 
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.template.loader import render_to_string
from rest_framework import status
from .utils import *

from .utils import *
from .serializers import *
from .models import *
from .permissions import *





class GoogleAuthRedirect(APIView):
    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri={settings.BASE_URL}/google/callback"
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
            "redirect_uri": settings.BASE_URL,
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
                user.is_email_verified = True
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
    def get(self, request, otp):
        otp = request.GET.get("otp")
        if not otp:
            return Response({"message": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Account.objects.get(otp=otp)
            user.is_email_verified = True
            user.save()
            return Response({"Message": "Account Verified"}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"message": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        


class CreateAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializers = AccountSerializer(data=request.data)
        data = {}
        if serializers.is_valid(raise_exception=False):
            user = serializers.save(is_buyer_user=True)
            user.otp = generate_otp()
            user.save()

            context = {
                "name": user.first_name,
                "verify_link": f"{settings.BASE_URL}/verify-email/?otp={user.otp}/",
                "subject": "Verify your Jumia account",
                "body": f"Hello {user.first_name},\n\nTo verify your Jumia account, please click on the link below:\n{settings.BASE_URL}/verify-email/?otp={user.otp}\n\nThank you!"
            }
            template = render_to_string("accounts/verify-email.html", context)
            send_email(user.email, "Verify your Jumia account", template)

            data["message"] = "Account created successfully."
            data["user_details"] = AccountSerializer(user).data
            data["tokens"] = jwt_auth(user)

            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    



class AccountLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid(raise_exception=False):
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            if email:
                try:
                    user = Account.objects.get(email=email)
                except Account.DoesNotExist:
                    return Response({"error": "User not found with this email."}, status=status.HTTP_404_NOT_FOUND)
            
            if password != user.password:
                return Response({"error": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
            
             
            
            data["response"] = "User logged in successfully"
            data["user_info"] = AccountSerializer(user).data
            data["Token"] = jwt_auth(user)
            return Response(data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ResetLinkView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        if request.user.is_authenticated:
            user = request.user
            email = user.email

        else:
            email = request.data.get('email')
            if not email:
                return Response({"Error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({"Error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.otp = generate_otp()
        reset_link = f"{settings.BASE_URL}/reset-password/?&otp={user.otp}"
        

        context = {
            "name": user.first_name or 'user',
            "reset_link": reset_link,
        }
        template = render_to_string("accounts/reset-password.html", context)
        send_email(email, "Reset your Jumia password", template)
        return Response({"message": "Reset link sent successfully."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request):
        serializers = ResetPasswordSerializer
        if serializers.is_valid():
            data = serializers.validated_data

            try:
                user = Account.objects.get(otp=data["otp"])
            except Account.DoesNotExist:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(data["password"])
            user.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class AccountDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user = request.user
        confirm = request.data.get("confirm")
        if not confirm or confirm.lower() != "yes":
            return Response({"error": "Please confirm deletion."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user.delete()
            return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)