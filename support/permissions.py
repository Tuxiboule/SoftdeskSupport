from rest_framework import permissions
import re

from support.models import Project
from support.models import Comment
from support.models import Issue


class IsSupervisor(permissions.BasePermission):
    """
    Custom permission to check if the user is a supervisor.

    Attributes:
        has_object_permission: Check if the user is a supervisor or the owner of the object.
        has_permission: Check if the user is a supervisor.
    """

    def has_object_permission(self, request, obj, view):
        """
        Check if the user is a supervisor or the owner of the object.

        Args:
            request: The HTTP request.
            view: The view that the permission is attached to.
            obj: The object for which permission is being checked.

        Returns:
            bool: True if the user is a supervisor or the owner, False otherwise.
        """
        user = request.user
        if user.is_supervisor or user == obj or user == view:
            return True
        else:
            return False

    def has_permission(self, request, view):
        """
        Check if the user is a supervisor.

        Args:
            request: The HTTP request.
            view: The view that the permission is attached to.

        Returns:
            bool: True if the user is a supervisor, False otherwise.
        """
        # Non-loged user creation
        if request.method == "POST" and request.path != "/api/contributor/":
            return True
        user = request.user
        pattern = re.compile(r"user/\d+/$")
        if pattern.search(request.path):
            return True
        return user.is_supervisor


class IsAuthorOrContributor(permissions.BasePermission):
    """
    Custom permission to check if the user is the author or a contributor to the object.

    Attributes:
        has_object_permission: Check if the user is the author or a contributor to the object.
        has_permission: Check if the user is a contributor to a specified project.
        is_contributor: Check if the user is a contributor to the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the author or a contributor to the object.

        Args:
            request: The HTTP request.
            view: The view that the permission is attached to.
            obj: The object for which permission is being checked.

        Returns:
            bool: True if the user is the author or a contributor, False otherwise.
        """
        user = request.user

        # If the user is the author, allow full access
        if obj.author == user:
            return True

        # If the user is a contributor and the action is in read-only mode, allow access
        if request.method in permissions.SAFE_METHODS and self.is_contributor(user, obj):
            return True

        return False

    def is_contributor(self, user, obj):
        """
        Check if the user is a contributor to the object.

        Args:
            user: The user for whom contribution is being checked.
            obj: The object to which the user might contribute.

        Returns:
            bool: True if the user is a contributor, False otherwise.
        """
        if isinstance(obj, Project):
            return obj.contributors.filter(username=user.username).exists()

        elif isinstance(obj, (Issue, Comment)) and hasattr(obj, 'project'):
            return obj.project.contributors.filter(username=user.username).exists()

        return False

    def has_permission(self, request, view):
        """
        Check if the user is a contributor to a specified project.

        Args:
            request: The HTTP request.
            view: The view that the permission is attached to.

        Returns:
            bool: True if the user is a contributor to the specified project, False otherwise.
        """
        match = re.match(r'^/api/project/(?P<project_id>\d+)/', request.path)
        if match is not None:
            project_id = match.group('project_id')
            project = Project.objects.get(id=project_id)
            user = request.user
            if project.contributors.filter(username=user.username).exists():
                return True
            else:
                return False
        else:
            return request.user.is_authenticated
