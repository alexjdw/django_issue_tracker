from apps.users.models import User
from apps.issues.models import Issue, Category
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializes a User object for the API.
    '''
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'issues_created',
                  'issues_owned', 'issues_joined')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializes a Category object for the API.
    '''
    class Meta:
        model = Category
        fields = ('id', 'name', 'issues')


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializies an Issue object for the API.
    '''
    class Meta:
        model = Issue
        fields = ('id', 'category', 'creator', 'owner', 'short', 'desc')