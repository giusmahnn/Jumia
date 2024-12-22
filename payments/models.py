import uuid
from django.db import models
from accounts.models import Account
from orders.models import Order
from .choices import Status


class UserWallet(models.Model):
    user = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation

    def __str__(self):
        return f"Wallet for {self.user.email}"



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    reference = models.CharField(max_length=100, unique=True, blank=True)  # Paystack transaction reference
    gateway_response = models.JSONField(blank=True, null=True)  # Raw response from Paystack
    status = models.CharField(max_length=10, choices=Status.choices, default='pending')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Payment timestamp
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"

    def save(self, *args, **kwargs):
        # Generate a unique reference if not already set
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)

    def generate_reference(self):
        # Generate a unique reference using user ID, order ID, and a UUID
        reference = f"PAY-{self.user.id}-{self.order.id}-{uuid.uuid4().hex[:10]}"
        while Payment.objects.filter(reference=reference).exists():
            reference = f"PAY-{self.user.id}-{self.order.id}-{uuid.uuid4().hex[:10]}"
        return reference
