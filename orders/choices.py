from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    PENDING = "Pending", _("Pending")
    SHIPPED = "Shipped", _("Shipped")
    DELIVERED = "Delivered", _("Delivered")
    CANCELLED = "Cancelled", _("Cancelled")
    COMPLETED = "Completed", _("Completed")
    RETURNED = "Returned", _("Returned")
    RETURN_REQUESTED = "Return Requested", _("Return Requested")
    RETURN_ACCEPTED = "Return Accepted", _("Return Accepted")
    RETURN_REJECTED = "Return Rejected", _("Return Rejected")
    