import uuid
from django.db import models
from authentification.models import User


class Comment(models.Model):
    """
    Model representing a comment on an issue.

    Attributes:
        date_created (DateTimeField): Date and time when the comment was created.
        date_updated (DateTimeField): Date and time when the comment was last updated.
        uuid (UUIDField): Unique identifier for the comment.
        description (TextField): Text content of the comment.
        author (ForeignKey): User who authored the comment.
        issue (ForeignKey): Issue to which the comment is associated
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='comments')


class Issue(models.Model):
    """
    Model representing an issue in a project.

    Attributes:
        date_created (DateTimeField): Date and time when the issue was created.
        date_updated (DateTimeField): Date and time when the issue was last updated.
        name (CharField): Name of the issue.
        description (TextField): Text content describing the issue.
        priority (CharField): Priority level of the issue (choices: LOW, MEDIUM, HIGH).
        beacon (CharField): Type of issue (choices: BUG, FEATURE, TASK).
        progress (CharField): Current progress status of the issue.
        author (ForeignKey): User who created the issue.
        project (ForeignKey): Project to which the issue is associated
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_author')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues')


class Project(models.Model):
    """
    Model representing a project.

    Attributes:
        date_created (DateTimeField): Date and time when the project was created.
        date_updated (DateTimeField): Date and time when the project was last updated.
        name (CharField): Name of the project.
        description (TextField): Text content describing the project.
        active (BooleanField): Indicates whether the project is active or not.
        type (CharField): Type of the project (choices: back-end, front-end, iOS, android).
        author (ForeignKey): User who created the project.
        contributors (ManyToManyField): Users contributing to the project through the Contributor model.
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=50,
                            choices=[('back-end', 'Back-End'),
                                     ('front-end', 'Front-End'),
                                     ('iOS', 'iOS'),
                                     ('android', 'Android')])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_author')
    contributors = models.ManyToManyField(User, through='Contributor', related_name='contributed_projects')


class Contributor(models.Model):
    """
    Model representing a contributor to a project.

    Attributes:
        date_created (DateTimeField): Date and time when the contribution relationship was created.
        date_updated (DateTimeField): Date and time when the contribution relationship was last updated.
        user (ForeignKey): User contributing to the project.
        project (ForeignKey): Project to which the user is contributing.
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributor_project')
