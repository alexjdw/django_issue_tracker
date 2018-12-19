from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from apps.users.models import User
from apps.issues.models import Issue


@login_required
def all_issues(request):
    return render(request, 'issues/all_issues.html')


@login_required
def my_issues(request):
    return render(request, 'issues/my_issues.html')


@login_required
def priority_issues(request):
    return render(request, 'issues/all_issues.html')


@login_required
def team_issues(request):
    return render(request, 'issues/team_issues.html')


@login_required
def issue(request, slug, issueno):
    # try:
    #     issue = Issue.objects.get(id=issueno)
    # except ObjectDoesNotExist:
    #     return redirect('/issues/all')

    return render(request, 'issues/issue.html', {'issue': issue})


@login_required
def create_issue(request):
    return redirect(request, 'issues/priority_issues.html')


@login_required
def create_form(request):
    return render(request, "issues/create.html")