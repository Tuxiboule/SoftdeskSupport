from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from support.models import Project
from support.models import Contributor


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    genre = serializers.ChoiceField(choices=Project._meta.get_field('type').choices)


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user']
