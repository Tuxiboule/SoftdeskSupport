from rest_framework import permissions

from support.models import Project
from support.models import Comment
from support.models import Issue


class IsAuthorOrContributor(permissions.BasePermission):
    """
    Permission to allow read-only access to contributors and full access to the author.
    """

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
        """
        Vérifie si l'utilisateur est un contributeur du projet associé à l'objet.
        """
        if isinstance(obj, Project):
            return obj.contributors.filter(user=user).exists()
        elif isinstance(obj, (Issue, Comment)) and hasattr(obj, 'project'):
            return obj.project.contributors.filter(user=user).exists()

        return False
    
    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est authentifié
        return request.user.is_authenticated