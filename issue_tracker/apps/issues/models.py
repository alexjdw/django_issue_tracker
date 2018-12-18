from django.db import models
from apps.users.models import User


class Issue(models.Model):
    creator = models.ForeignKey(User, related_name="issues_created")
    owner = models.ForeignKey(User, related_name="issues_owned", null=True)
    users = models.ManyToManyField(User, related_name="issues_joined", null=True)
    title = models.CharField(max_length=40)
    short = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    priority = models.PositiveSmallIntegerField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)


class IssueLogEntry(models.Model):
    creator = models.ForeignKey(User, related_name="log_entries")
    issue = models.ForeignKey(Issue, related_name="log_entries")
    entry = models.CharField(max_length=500)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
