from django.db import models
from apps.users.models import User
import json

class Category(models.Model):
    '''
    Issues are categorized for searching using this model.

    :name: The name of the category.

    Category has a 1:Many relationship with Issue. In the future, a
    Many:Many relationship is planned.
    '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Category Object: <name: {self.name}>"


class IssueManager(models.Manager):
    '''
    Manager class for Issue.

    :validate_and_create: Creates and returns a new issue from a POST request.
    Requires 'category', 'shortdesc', 'desc', and 'severity' to be in the POST
    data. Can also accept any key/value store.

    Returns a dict of validation error messages if it fails to create.
    '''
    def validate_and_create(self, post, creator):
        errors = {}

        for item in ['category', 'shortdesc', 'desc', 'severity']:
            if item not in post:
                return {'form': 'Please fill in all required fields.'}
            else:
                if len(item) < 1:
                    return {'form': 'Please fill in all required fields.'}

        if len(post['desc']) < 10:
            errors['desc'] = "Please enter at least 10 characters for the description."
        if len(post['shortdesc']) < 10:
            errors['shortdesc'] = "Please enter at least 10 characters for the short description."
        if 1 > int(post['severity']) > 5:
            errors['severity'] = "Severity must be between 1 and 5."

        category = Category.objects.filter(name=post['category']).first()
        category = Category.objects.filter(name=post['category']).first()
        if not category:
            category = Category.objects.create(name=post['category'])

        if errors == {}:
            return self.create(creator=creator,
                               category=category,
                               short=post['shortdesc'],
                               desc=post['desc'],
                               priority=post['severity']
                               )
        return errors


class Issue(models.Model):
    '''
    The core model for this project, representing a bug, feature request,
    or some other completable task.

    :creator: User that submitted the issue.
    :owner: A user that has taken responsibility for resolving the issue.
    :users: Users that are "watching" the issue.
    :category: Searchable term that succintly groups the issue with related issues.
    :short: Short description that fits on a post-it card.
    :desc: Long description.
    :priority: Severity of issue from 1-5.
    :log_entries: 1:Many link to IssueLogEntry.
        Used for posting short memos to the issue page for others to view.
    '''
    creator = models.ForeignKey(User, related_name="%(class)ss_created")
    owner = models.ForeignKey(User, related_name="%(class)ss_owned", null=True)
    users = models.ManyToManyField(User, related_name="%(class)ss_joined")
    category = models.ForeignKey(Category, related_name="%(class)ss")
    short = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    priority = models.PositiveSmallIntegerField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    objects = IssueManager()

    @classmethod
    def from_issue(cls, issue):
        # works for issues or resolved issues
        newissue = cls(
            creator=issue.creator,
            owner=issue.owner,
            category=issue.category,
            short=issue.short,
            desc=issue.desc,
            priority=issue.priority,
            created_on=issue.created_on,
            updated_on=issue.updated_on,
            )
        newissue.save()
        for user in issue.users.all():
            newissue.users.add(user)
        newissue.save()

        return newissue

    def __repr__(self):
        return f"Issue Object: <{self.category.name}-{self.id} {self.created_on}>"


class ResolvedIssue(models.Model):
    '''
    Resolved issue. See Issue. At this time, issue ID is not preserved when
    marking an issue resolved.
    '''
    old_id = models.IntegerField()
    creator = models.ForeignKey(User, related_name="%(class)ss_created")
    owner = models.ForeignKey(User, related_name="%(class)ss_owned", null=True)
    users = models.ManyToManyField(User, related_name="%(class)ss_joined")
    category = models.ForeignKey(Category, related_name="%(class)ss")
    short = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    priority = models.PositiveSmallIntegerField()
    created_on = models.DateField()
    updated_on = models.DateField(auto_now=True)
    resolved_on = models.DateTimeField(auto_now_add=True)
    serialized_log = models.TextField(null=True)
    objects = IssueManager()

    @classmethod
    def from_issue(cls, issue):
        # works for issues or resolved issues
        newissue = cls(
            old_id=issue.id,
            creator=issue.creator,
            owner=issue.owner,
            category=issue.category,
            short=issue.short,
            desc=issue.desc,
            priority=issue.priority,
            created_on=issue.created_on,
            updated_on=issue.updated_on,
            )
        newissue.save()
        for user in issue.users.all():
            newissue.users.add(user)

        logs = ''.join([log.to_json() for log in issue.log_entries.all()])
        newissue.serialized_log = logs
        newissue.save()

        return newissue

    def __repr__(self):
        return f"Issue Object: <{self.category.name}-{self.id} {self.created_on}>"


class IssueLogEntry(models.Model):
    '''
    Log entry for users to make comments on an issue.
    '''
    creator = models.ForeignKey(User, related_name="log_entries")
    issue = models.ForeignKey(Issue, related_name="log_entries")
    entry = models.CharField(max_length=500)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def to_json(self):
        return json.dumps({
            'creator': self.creator,
            'entry': self.entry,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        })
