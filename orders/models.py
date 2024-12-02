from django.db import models

from accounts.models import *
from .choices import Status
from products.models import Product

class Order(models.Model):  
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_orders")  
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="customer_orders")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")  
    quantity = models.PositiveIntegerField()  
    status = models.CharField(max_length=20, choices=Status.choices, default='pending')  
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} - {self.status}"


class VendorReview(models.Model):
    """
    Represents customer reviews and ratings for a vendor.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="vendor_reviews")
    rating = models.PositiveIntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.vendor.store_name} by {self.customer.username}"
