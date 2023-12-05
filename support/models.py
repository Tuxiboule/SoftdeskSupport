from django.db import models
from django.contrib.auth.models import AbstractUser

from authentification.models import User


class Project(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=50,
                            choices=[('back-end', 'Back-End'),
                                     ('front-end', 'Frond-End'),
                                     ('iOS', 'iOS'),
                                     ('android', 'Android')])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    is_creator = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
