from django.forms import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Account
import datetime
import random
import re



def generate_otp(*, k=6):
    return ''.join(random.choices('0123456789', k=k))



def jwt_auth(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    return {
        "refresh_token": str(refresh_token),
        "access_token": str(access_token),
    }



def send_email(user_email, subject, template):
    subject = subject
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=subject,
        body="Email Content",
        from_email=from_email,
        to= to_email
    )
    email.content_subtype = "html"
    email.attach_alternative(template, "text/html")

    try:
        email.send(fail_silently=False)
    except Exception as e:
        print(f"Failed to send email to {user_email}: {str(e)}")
        return "Couldn't send email"
    
    return None



def validate_otp(user_email, otp, ttl_minutes=5):
    try:
        user = Account.objects.filter(email=user_email).first()
    except Account.DoesNotExist:
        return False
    
    if not user.otp or not user.otp_created_at or datetime.timezone.now() > datetime.timedelta(minutes=ttl_minutes):
        user.reset_otp()
        return "The OTP has expired, please request a new one."  # OTP expired

    if user.otp == otp:
        user.reset_otp()
        return "OTP validated successfully"
    return "Invalid OTP"





def validate_password(value):
    if len(value) < 8:
        raise ValidationError(
            "Password must be at least 8 characters long")
    if not any(char.isdigit() for char in value):
        raise ValidationError(
            "Password must contain at least one digit")
    if not any(char.isalpha() for char in value):
        raise ValidationError(
            "Password must contain at least one letter")
    if not any(char.islower() for char in value):
        raise ValidationError(
            "Password must contain at least one lowercase letter")
    if not any(char.isupper() for char in value):
        raise ValidationError(
            "Password must contain at least one uppercase letter")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(
            "Password must contain at least one special character")
    return True