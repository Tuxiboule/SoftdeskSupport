from rest_framework.serializers import ModelSerializer
from support.models import Project
from support.models import Contributor
from support.models import Issue
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

    class Meta:
        model = Issue
        fields = '__all__'