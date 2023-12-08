"""SoftdeskSupport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentification.views import UserViewSet
from support.views import ProjectViewSet
from support.views import ContributorViewSet
from support.views import IssueViewSet
from support.views import CommentViewSet

router = routers.SimpleRouter()
router.register('user', UserViewSet, basename='user')
router.register('project', ProjectViewSet, basename='project')
router.register('contributor', ContributorViewSet, basename="contributor")
router.register(r'project/(?P<project_id>\d+)/issue',
                IssueViewSet, basename='project-issue')
router.register('issue', IssueViewSet, basename='issue')
router.register(r'project/(?P<project_id>\d+)/issue/(?P<issue_id>\d+).comment',
                CommentViewSet, basename='issue-comment')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
