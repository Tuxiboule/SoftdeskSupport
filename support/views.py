from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from support.serializers import ProjectSerializer
from support.serializers import ContributorSerializer
from support.serializers import IssueSerializer

from support.models import Project
from support.models import Contributor
from support.models import Issue

# Create your views here.


class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()