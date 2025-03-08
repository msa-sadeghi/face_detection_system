from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False, verbose_name=_("مدیر"))  # manager role
