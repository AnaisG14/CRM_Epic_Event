from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SAILOR = 'SAILOR'
    SUPPORT = 'SUPPORT'
    MANAGER = 'MANAGER'

    ROLE_CHOICES = (
        (SAILOR, 'Sailor team'),
        (SUPPORT, 'Support team'),
        (MANAGER, 'Management team'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=False, null=False)

    def __str__(self):
        return f"{self.username} {self.role}"


