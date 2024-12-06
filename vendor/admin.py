from django.contrib import admin

from vendor.models import Vendor, VendorReview

# Register your models here.
admin.site.register(Vendor)
admin.site.register(VendorReview)