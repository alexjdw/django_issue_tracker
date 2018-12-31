from apps.users.models import User
from apps.issues.models import Issue, Category
from .serializers import UserSerializer, CategorySerializer, IssueSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    '''
    Renders a User serialized object.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IssueViewSet(viewsets.ModelViewSet):
    '''
    Renders an Issue serialized object.
    '''
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''
    Renders a Category serialized object.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
