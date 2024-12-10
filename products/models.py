# File: products/models.py

from django.db import models
from .choices import *

from vendor.models import Vendor


class Product(models.Model):
    """
    Represents a product, now linked to a vendor.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.CharField(max_length=30, null=True, blank=True, choices=Category.choices)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/',
                              default="product_images/default-product-image.png", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_on_sale(self):
        return self.discount_price is not None

    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return round((1 - (self.discount_price / self.price)) * 100, 2)
        return 0
