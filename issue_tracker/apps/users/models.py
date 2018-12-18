from django.db import models
from django.contrib.auth.models import User


class RegKey(models.Model):
    '''Keys for registering users.'''
    regkey = models.CharField(max_length=255, unique=True)
    already_used = models.BooleanField(default=False)