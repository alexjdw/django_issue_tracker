from django.db import models
from django.contrib.auth.models import User


class Permissions(models.Model):
    adminpage = models.BooleanField()
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name="permissions")


class RegKey(models.Model):
    '''Keys for registering users.'''
    regkey = models.CharField(max_length=255, unique=True)