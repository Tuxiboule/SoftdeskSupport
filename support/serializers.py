from rest_framework.serializers import ModelSerializer
from support.models import Project
from support.models import Contributor
from support.models import Issue
from support.models import Comment
from authentification.serializers import UserSerializer
from rest_framework import serializers


class ProjectSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)
    contributors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors', 'active']
        read_only_fields = ['author']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        project = Project.objects.create(**validated_data)
        Contributor.objects.create(user=user, project=project)
        return project


class ContributorSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = '__all__'


class IssueSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author', 'project']

    def create(self, validated_data):
        project_id = self.context['request'].resolver_match.kwargs.get('project_id')
        user = self.context['request'].user
        validated_data['author'] = user
        project = Project.objects.get(id=project_id)
        Contributor.objects.create(user=user, project=project)
        validated_data['project'] = project
        issue = Issue.objects.create(**validated_data)
        return issue


class CommentSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'project']

    def create(self, validated_data):
        project_id = self.context['request'].resolver_match.kwargs.get('project_id')
        issue_id = self.context['request'].resolver_match.kwargs.get('issue_id')
        user = self.context['request'].user
        validated_data['author'] = user
        validated_data['issue'] = Issue.objects.get(id=issue_id)
        project = Project.objects.get(id=project_id)
        Contributor.objects.create(user=user, project=project)
        comment = Comment.objects.create(**validated_data)
        return comment
