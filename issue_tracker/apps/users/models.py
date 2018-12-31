from django.db import models
from django.contrib.auth.models import User


class Permissions(models.Model):
    '''
    A 1:1 extension of users. Has boolean user permissions.

    :adminpage: Access to app-based administration routes. (Does not include
    Django's admin pages.)
    '''
    adminpage = models.BooleanField()
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name="permissions")


class RegKey(models.Model):
    '''
    Keys for registering users.
    '''
    regkey = models.CharField(max_length=255, unique=True)