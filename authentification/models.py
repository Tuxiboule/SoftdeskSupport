from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    birthdate = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField()
    can_be_shared = models.BooleanField()

    def create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(extra_fields['password'])
        user.save(using=self._db)
        return user
