from django.db import models

from accounts.models import Account

# # Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="vendor")
    store_logo = models.ImageField(
        upload_to="store_logo/", default="store_logo/default-profile-image.png", blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    store_description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nationality = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} | {self.store_name}"



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