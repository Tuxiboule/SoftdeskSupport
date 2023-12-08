from rest_framework import permissions


class IsAuthorOrContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        print("______________", obj)
        print("______________", view)

        if obj.author == request.user:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
