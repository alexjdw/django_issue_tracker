from apps.users.models import User
from apps.issues.models import Issue, Category
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'issues_created',
                  'issues_owned', 'issues_joined')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'issues')


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'category', 'creator', 'owner', 'short', 'desc')