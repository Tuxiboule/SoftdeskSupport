from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    birthdate = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField()
    can_be_shared = models.BooleanField()