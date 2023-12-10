from rest_framework.viewsets import ModelViewSet
from support.permissions import IsAuthorOrContributor
from django.shortcuts import get_object_or_404

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

    permission_classes = [IsAuthorOrContributor]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        contributor_projects = Contributor.objects.filter(user=user).values_list('project', flat=True)
        return Project.objects.filter(id__in=contributor_projects)


class ContributorViewSet(ModelViewSet):

    #permission_classes = [IsAuthorOrContributor]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewSet(ModelViewSet):

    permission_classes = [IsAuthorOrContributor]
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        user = self.request.user
        if user in project.contributors.all():
            issues = project.issues.all()
            return issues
        else:
            return Issue.objects.none()


class CommentViewSet(ModelViewSet):

    permission_classes = [IsAuthorOrContributor]
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        issue = Issue.objects.get(id=issue_id)

        return issue.comments.all()
