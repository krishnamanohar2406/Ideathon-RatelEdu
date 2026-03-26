from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_active_for_study = models.BooleanField(default=False)


    