from django.db import models
from django.utils.translation import gettext_lazy as _





class Category(models.TextChoices):
    ELECTRONICS = "Electronics", _("Electronics")
    TOOLS = "Tools", _("Tools")
    FURNITURE = "Furniture", _("Furniture")
    PHONE = "Phone", _("Phone")
    ACCESSORIES = "Accessories", _("Accessories")
    HOME_APPLIANCES = "Home Appliances", _("Home Appliances")
    LAPTOP = "Laptop", _("Laptop")
    COMPUTER_ACCESSORIES = "Computer Accessories", _("Computer Accessories")
    CAMERA = "Camera", _("Camera")
    GADGETS = "Gadgets", _("Gadgets")
    WATCHES = "Watches", _("Watches")
    CLOTHING = "Clothing", _("Clothing")
    SHOES = "Shoes", _("Shoes")
    JEWELRY = "Jewelry", _("Jewelry")
    BABY_PRODUCTS = "Baby Products", _("Baby Products")
    BEAUTY = "Beauty", _("Beauty")
    KITCHEN_APPLIANCES = "Kitchen Appliances", _("Kitchen Appliances")
    FOODS = "Foods", _("Foods")
    OTHERS = "OTHERS", _("Others")