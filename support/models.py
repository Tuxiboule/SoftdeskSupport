from django.db import models
from authentification.models import User


class Project(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=50,
                            choices=[('back-end', 'Back-End'),
                                     ('front-end', 'Frond-End'),
                                     ('iOS', 'iOS'),
                                     ('android', 'Android')])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_author')
    contributors = models.ManyToManyField(User, through='Contributor', related_name='contributed_projects')


class Contributor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributor_project')


class Issue(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_author')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    priority = models.CharField(max_length=50,
                                choices=[('LOW', 'LOW'),
                                         ('MEDIUM', 'MEDIUM'),
                                         ('HIGH', 'HIGH')])
    beacon = models.CharField(max_length=50,
                              choices=[('BUG', 'BUG'),
                                       ('FEATURE', 'FEATURE'),
                                       ('TASK', 'TASK')])
    progress = models.CharField(max_length=50,
                                choices=[('To Do', 'To do'),
                                         ('In Progress', 'In Progress'),
                                         ('Finished', 'Finished')],
                                default="To Do")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
