from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_data = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.username