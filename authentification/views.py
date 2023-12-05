from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from authentification.models import User
from authentification.serializers import UserSerializer

# Create your views here.


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()