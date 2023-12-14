from rest_framework.viewsets import ModelViewSet 

from authentification.models import User
from authentification.serializers import UserSerializer

from support.permissions import IsSupervisor


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.

    This viewset uses the UserSerializer for serialization and supports
    standard CRUD operations.

    Attributes:
        serializer_class (UserSerializer): Serializer class for User model.
        permission_classes (list): List of permission classes, in this case, IsSupervisor.

    Methods:
        get_queryset(): Retrieve the queryset for this view.
    """

    serializer_class = UserSerializer
    permission_classes = [IsSupervisor]

    def get_queryset(self):
        """
        Retrieve the queryset for this view.

        Returns:
            queryset: All User objects.
        """
        return User.objects.all()
