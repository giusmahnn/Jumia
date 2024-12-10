from django.db import models

from accounts.models import *
from vendor.models import Vendor
from .choices import Status
from products.models import Product

class Order(models.Model):  
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_orders")  
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="customer_orders")  
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")  
    # quantity = models.PositiveIntegerField()  
    status = models.CharField(max_length=20, choices=Status.choices, default='pending')  
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.status}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"




# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price




# Shipping address model
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipping_address")
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)


    def __str__(self):
        return f"Shipping Address for {self.customer.email}"

    def get_full_address(self):
        return f"{self.address_line_1}, {self.address_line_2 or ''}, {self.city}, {self.state}, {self.postal_code}, {self.country}".strip(", ")