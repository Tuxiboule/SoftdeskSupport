from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from support.models import Project
from support.models import Contributor
from support.models import Issue
from support.models import Comment


class CommentSerializer(ModelSerializer):
    """
    Serializer for Comment model.

    Attributes:
        author (UserSerializer): Serializer for the author of the comment.
    """
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'issue']

    def create(self, validated_data):
        """
        Create a new comment instance with validated data.

        Args:
            validated_data (dict): Validated data for creating the comment.

        Returns:
            Comment: Newly created Comment instance.
        """
        user = self.context['request'].user
        issue_id = self.context['request'].resolver_match.kwargs.get('issue_id')
        issue = Issue.objects.get(id=issue_id)

        project = Project.objects.filter(issues__id=issue_id).first()
        if user not in project.contributors.all():
            return "user not in contributors please sub to project"

        validated_data['author'] = user
        validated_data['issue'] = issue
        comment = Comment.objects.create(**validated_data)
        return comment


class IssueSerializer(ModelSerializer):
    """
    Serializer for Issue model.

    Attributes:
        author (UserSerializer): Serializer for the author of the issue.
        comments (CommentSerializer): Serializer for the comments associated with the issue.
    """

    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author', 'project']

    def create(self, validated_data):
        """
        Create a new issue instance with validated data.

        Args:
            validated_data (dict): Validated data for creating the issue.

        Returns:
            Issue: Newly created Issue instance.
        """
        user = self.context['request'].user
        project_id = self.context['request'].resolver_match.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        validated_data['author'] = user
        validated_data['project'] = project
        issue = Issue.objects.create(**validated_data)
        return issue


class ProjectSerializer(ModelSerializer):
    """
    Serializer for Project model.

    Attributes:
        author (UserSerializer): Serializer for the author of the project.
        contributors (StringRelatedField): Serializer for contributors to the project.
        issues (IssueSerializer): Serializer for the issues associated with the project.
    """

    issues = IssueSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'issues', 'author', 'contributors', 'active']
        read_only_fields = ['author']

    def create(self, validated_data):
        """
        Create a new project instance with validated data.

        Args:
            validated_data (dict): Validated data for creating the project.

        Returns:
            Project: Newly created Project instance.
        """
        user = self.context['request'].user
        validated_data['author'] = user
        project = Project.objects.create(**validated_data)
        Contributor.objects.create(user=user, project=project)
        return project


class ContributorSerializer(ModelSerializer):
    """
    Serializer for Contributor model.
    """

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']

    def create(self, validated_data):
        """
        Create a new contributor instance with validated data.

        Args:
            validated_data (dict): Validated data for creating the contributor.

        Returns:
            Contributor: Newly created Contributor instance.
        """
        user = validated_data.get('user')
        project = validated_data.get('project')

        existing_contributor = Contributor.objects.filter(user=user, project=project).first()

        if existing_contributor:
            raise serializers.ValidationError("L'utilisateur est déjà contributeur sur ce projet")

        contributor = Contributor.objects.create(**validated_data)
        return contributor
