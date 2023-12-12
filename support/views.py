from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

import re

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

        user = self.request.user
        contributions = user.contributions.all()
        projects = [contribution.project for contribution in contributions]
        # No detail asked
        if re.match(r'^/api/project/$', self.request.path):
            return projects
        # Detail about a project
        else:
            match = re.match(r'^/api/project/(?P<project_id>\d+)/$', self.request.path)
            project_id = match.group('project_id')
            project = Project.objects.filter(id=project_id)
            if project[0] in projects:
                return project
            else:
                return Project.objects.none()


class ContributorViewSet(ModelViewSet):

    # permission_classes = ISSUPERVISOR
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        user = self.request.user
        contributions = user.contributions.all()
        contributed_projects_id = [contribution.project.id for contribution in contributions]
        
        match = re.match(r'^/api/project/(?P<project_id>\d+)/', self.request.path)
        project_id = match.group('project_id')
        if str(project_id) in map(str, contributed_projects_id):
            return Issue.objects.filter(project=project_id)
        else:
            return Issue.objects.none()


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrContributor]

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        issue = Issue.objects.get(id=issue_id)

        return issue.comments.all()
