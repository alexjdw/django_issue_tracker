from django.db import models
from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Category Object: <name: {self.name}>"


class IssueManager(models.Manager):
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
        for user in issue.users.all():
            newissue.users.add(user)

        return newissue

    def __repr__(self):
        return f"Issue Object: <{self.category.name}-{self.id} {self.created_on}>"


class ResolvedIssue(models.Model):
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
        for user in issue.users.all():
            newissue.users.add(user)

        return newissue

    def __repr__(self):
        return f"Issue Object: <{self.category.name}-{self.id} {self.created_on}>"


class IssueLogEntry(models.Model):
    creator = models.ForeignKey(User, related_name="log_entries")
    issue = models.ForeignKey(Issue, related_name="log_entries")
    entry = models.CharField(max_length=500)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
