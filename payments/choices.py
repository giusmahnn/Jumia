from django.db import models
from django.utils.translation import gettext_lazy as _



class Status(models.TextChoices):
    PENDING = "Pending", _("Pending")
    SUCCESSFUL = "Successful", _("Successful")
    FAILED = "Failed", _("Failed")