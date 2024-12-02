# from django.db import models

# from accounts.models import Account

# # Create your models here.
# class Vendor(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     store_logo = models.ImageField(
#         upload_to="store_logo/", default="store_logo/default-profile-image.png", blank=True, null=True)
#     store_name = models.CharField(max_length=255, blank=True, null=True)
#     store_description = models.TextField(blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     nationality = models.CharField(max_length=20, null=True, blank=True)
#     state = models.CharField(max_length=20, null=True, blank=True)
#     city = models.CharField(max_length=20, null=True, blank=True)
#     address = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.email} | {self.store_name}"