from rest_framework.viewsets import ModelViewSet
from support.permissions import IsAuthorOrContributor

from support.serializers import ProjectSerializer
from support.serializers import ContributorSerializer
from support.serializers import IssueSerializer
from support.serializers import CommentSerializer

from support.models import Project
from support.models import Contributor
from support.models import Issue
from support.models import Comment

# Create your views here.


class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        return Project.objects.all()


class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        return Comment.objects.all()
