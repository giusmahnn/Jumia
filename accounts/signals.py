from datetime import timezone
from django.db.models.signals import post_save
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

from .utils import *
from .models import Account

@receiver(post_save, sender=Account)
def verify_email(sender, instance, created, **kwargs):
    if created and not instance.is_email_verified:
        # Generate and save the OTP
        instance.otp = generate_otp()
        instance.otp_created_at = timezone.now()
        instance.save()

        # Build the verification URL
        current_site = get_current_site(None)  # Fetch domain dynamically
        verification_url = f"http://{current_site.domain}{reverse('verify-email')}?otp={instance.otp}"

        # Send verification email
        try:
            send_email(
                "Verify Your Email",
                f"Click the link to verify your email: {verification_url}",
                "no-reply@myapp.com",
                [instance.email],
            )
        except Exception as e:
            # Log the email sending error (you can replace with a logging system)
            print(f"Failed to send verification email to {instance.email}: {e}")