from rest_framework import permissions
import re

from support.models import Project
from support.models import Comment
from support.models import Issue
from support.models import Contributor


class IsAuthorOrContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Si l'utilisateur est l'auteur, autoriser l'accès complet
        if obj.author == user:
            return True

        # Si l'utilisateur est un contributeur et l'action est en lecture seule, autoriser l'accès
        if request.method in permissions.SAFE_METHODS and self.is_contributor(user, obj):
            return True

        return False

    def is_contributor(self, user, obj):
        if isinstance(obj, Project):
            return obj.contributors.filter(username=user.username).exists()

        elif isinstance(obj, (Issue, Comment)) and hasattr(obj, 'project'):
            return obj.project.contributors.filter(username=user.username).exists()

        return False

    def has_permission(self, request, view):
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
