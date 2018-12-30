from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse

from .models import User, Issue, ResolvedIssue, IssueLogEntry


@login_required
def all_issues(request):
    issues = Issue.objects.all().order_by("-created_on")
    return render(request, 'issues/all_issues.html', {'issues': issues})


@login_required
def my_issues(request):
    owned = Issue.objects.filter(owner=request.user).order_by("-created_on")
    joined = request.user.issues_joined.all()
    context = {
        'owned_issues': owned,
        'joined_issues': joined
        }
    return render(request, 'issues/my_issues.html', context)


@login_required
def priority_issues(request):
    return render(request, 'issues/all_issues.html')


@login_required
def team_issues(request):
    return render(request, 'issues/team_issues.html')


@login_required
def issue(request, issueno, category=None):
    try:
        issue = Issue.objects.get(id=issueno)
    except ObjectDoesNotExist:
        messages.error(
            request, "Issue doesn't exist. Are you sure you got the right issue id?")
        return redirect('/issues/all')
    if category is not None and issue.category.name != category:
        messages.error(
            request, "URL category doesn't match the issue. Are you sure you got the right issue id?")
        return redirect('/issues/all')

    return render(request, 'issues/issue.html', {'issue': issue})


@login_required
def create_form_submit(request):
    if request.method != "POST":
        return redirect(create_issue)

    issue = Issue.objects.validate_and_create(
        post=request.POST, creator=request.user)
    if isinstance(issue, dict):
        return redirect('/issues/new')
    return redirect(f'/issues/{issue.category.name}-{issue.id}')


@login_required
def create_form(request):
    return render(request, "issues/create.html")


@login_required
def join_issue(request, issueno, category=None):
    try:
        issue = Issue.objects.get(id=issueno)
    except ObjectDoesNotExist:
        messages.error(request, 'Issue not found. It may have been removed.')
        return redirect('/issues/all')

    if request.user not in issue.users.all():
        issue.users.add(request.user)
        issue.save()
    else:
        messages.warning(request, 'You are already watching this issue.')

    return redirect('/issues/' + issue.category.name + '-' + str(issue.id))


@login_required
def own_issue(request, issueno, category=None):
    try:
        issue = Issue.objects.get(id=issueno)
    except ObjectDoesNotExist:
        messages.error(request, 'Issue not found. It may have been removed.')
        return redirect('/issues/all')

    if issue.owner is not None:
        messages.error(request, 'This issue alread has an owner: ' +
                       issue.owner.first_name + " " + issue.owner.last_name)
        print("Error")
    else:
        print(issue.owner)
        issue.owner = request.user
        print("Owner assigned", issue.owner)
        issue.save()
    return redirect('/issues/' + issue.category.name + '-' + str(issue.id))


@login_required
def watch_issue(request, issueno, category=None):
    return redirect('/issues/' + issue.category.name + '-' + str(issue.id))


@login_required
def add_to_log(request, issueno, category=None):
    if request.method != 'POST':
        messages.error(request, 'Got an invalid request type:' + request.type)
        return redirect('/issues/all')

    try:
        issue = Issue.objects.get(id=issueno)
    except ObjectDoesNotExist:
        messages.error(request, 'Issue not found. It may have been removed.')
        return redirect('/issues/all')

    logentry = IssueLogEntry.objects.create(creator=request.user,
                                            issue=issue,
                                            entry=request.POST['logtext'],
                                            )
    if logentry is None:
        messages.error(request, 'Log entry failed to create for some reason.')
        return redirect('/issues/' + issue.category.name + '-' + str(issue.id))

    return redirect('/issues/' + issue.category.name + '-' + str(issue.id))


@login_required
def mark_complete(request, issueno):
    issue = Issue.objects.get(id=issueno)
    res = ResolvedIssue.from_issue(issue)
    res.save()

    issue.delete()

    return HttpResponse('')


@login_required
def drop_issue(request, issueno):
    issue = Issue.objects.get(id=issueno)
    request.user.issues_joined.remove(issue)
    request.user.save()

    return HttpResponse('')
