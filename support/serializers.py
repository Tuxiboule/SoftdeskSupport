from rest_framework.serializers import ModelSerializer
from support.models import Project
from support.models import Contributor
from support.models import Issue
from support.models import Comment
from authentification.serializers import UserSerializer
from rest_framework import serializers


class CommentSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'project']
    
    def create(self, validated_data):

        user = self.context['request'].user
        issue_id = self.context['request'].resolver_match.kwargs.get('issue_id')
        issue = Issue.objects.get(id=issue_id)

        project = Project.objects.filter(issues__id=issue_id).first()
        if user not in project.contributors.all():
            Contributor.objects.create(user=user, project=project)

        validated_data['author'] = user
        comment = Comment.objects.create(**validated_data)
        issue.comments.add(comment)
        return comment


class IssueSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author', 'project']

    def create(self, validated_data):
        user = self.context['request'].user
        project_id = self.context['request'].resolver_match.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        if user not in project.contributors.all():
            Contributor.objects.create(user=user, project=project)

        validated_data['author'] = user
        issue = Issue.objects.create(**validated_data)
        project.issues.add(issue)
        return issue


class ProjectSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)
    contributors = serializers.StringRelatedField(many=True, read_only=True)
    issues = IssueSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'issues', 'author', 'contributors', 'active']
        read_only_fields = ['author']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        project = Project.objects.create(**validated_data)
        Contributor.objects.create(user=user, project=project)
        return project


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
