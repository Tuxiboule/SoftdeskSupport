"""SoftdeskSupport URL Configuration

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views:
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views:
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
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

# Create a SimpleRouter for API endpoints
router = routers.SimpleRouter()
router.register('user', UserViewSet, basename='user')
router.register('project', ProjectViewSet, basename='project')
router.register('contributor', ContributorViewSet, basename="contributor")

# Create a NestedRouter for issue and comment endpoints
nested_router = routers.NestedSimpleRouter(router, r'project', lookup='project')
nested_router.register(r'issue', IssueViewSet, basename='project-issue')
nested_router.register(r'issue/(?P<issue_id>\d+)/comment', CommentViewSet, basename='issue-comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Include the main router's URLs
    path('api/', include(router.urls)),

    # Include the nested router's URLs
    path('api/', include(nested_router.urls)),
]
