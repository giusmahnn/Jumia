from django.forms import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Account
import datetime
import random
import re



def generate_otp(length=6):
    return ''.join(random.choice("0123456789", length))



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



def validate_otp(user_email, otp, ttl_minutes=10):
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
        raise ValidationError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValidationError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", value):
        raise ValidationError("Password must contain at least one digit")
    if not re.search(r"[^A-Za-z0-9]", value):
        raise ValidationError("Password must contain at least one special character")
    return True