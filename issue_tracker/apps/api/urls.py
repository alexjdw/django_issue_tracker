from django.conf.urls import url, include
from .serializers import UserSerializer, IssueSerializer, CategorySerializer
from .viewsets import UserViewSet, IssueViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]