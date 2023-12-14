from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that extends AbstractUser.

    Attributes:
        birthdate (DateField): User's birthdate
        can_be_contacted (BooleanField): Indicates if the user can be contacted.
        can_be_shared (BooleanField): Indicates if the user's information can be shared.
        is_supervisor (BooleanField): Indicates if the user is a supervisor, default is False.
    """

    birthdate = models.DateField(help_text="User's birthdate, can be null or blank.")
    can_be_contacted = models.BooleanField(help_text="Indicates if the user can be contacted.")
    can_be_shared = models.BooleanField(help_text="Indicates if the user's information can be shared.")
    is_supervisor = models.BooleanField(default=False, help_text="Indicates if the user is a supervisor, default is False.")
