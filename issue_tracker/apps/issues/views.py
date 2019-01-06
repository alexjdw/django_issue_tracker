from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from .models import Issue, ResolvedIssue, IssueLogEntry, Category
from django.db.models import Q


@login_required
def all_issues(request):
    '''
    Displays all issues.
    '''
    issues = Issue.objects.all().order_by("-created_on")
    return render(request, 'issues/all_issues.html', {'issues': issues})


@login_required
def my_issues(request):
    '''
    Displays the current user's owned and joined issues.
    '''
    owned = Issue.objects.filter(owner=request.user).order_by("-created_on")
    joined = request.user.issues_joined.all()
    context = {
        'owned_issues': owned,
        'joined_issues': joined
        }
    return render(request, 'issues/my_issues.html', context)


@login_required
def priority_issues(request):
    '''
    Awaiting implementation.
    '''
    return render(request, 'issues/all_issues.html')


@login_required
def team_issues(request):
    '''
    Awaiting implementation.
    '''
    return render(request, 'issues/team_issues.html')


@login_required
def issue(request, issueno, category=None):
    '''
    Renders the details for a single issue.

    :issueno: The issue's database ID.
    :category: The issue's category name.

    (Category doesn't matter as we pull issues directly from the issueno, but
    we do check if it matches.)
    '''
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
    '''
    POST route for creating a new issue via the create form.
    '''
    if request.method != "POST":
        return redirect(create_form)

    issue = Issue.objects.validate_and_create(
        post=request.POST, creator=request.user)
    if isinstance(issue, dict):
        return redirect('/issues/new')
    return redirect(f'/issues/{issue.category.name}-{issue.id}')


@login_required
def create_form(request):
    '''
    Route that renders the create issue form.
    '''
    return render(request, "issues/create.html")


@login_required
def join_issue(request, issueno, category=None):
    '''
    Route for adding an issue to your watch list.
    '''
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
    '''
    Route for taking ownership of an issue. User will appear as the "Lead" on the issue.
    '''
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
def add_to_log(request, issueno, category=None):
    '''
    POST route for adding to the "log" section for a single issue.
    '''
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
def all_categories(request):
    context = {
        'categories': Category.objects.all()
    }

    return render(request, 'issues/all_categories.html', context)


@login_required
def one_category(request, category):
    try:
        context = {
                    'category': Category.objects.get(name=category)
                  }
    except ObjectDoesNotExist:
        messages.error(request, "Category doesn't exist.")
        return redirect(all_categories)

    return render(request, 'issues/category.html', context)


@login_required
def mark_complete(request, issueno):
    '''
    Route for marking an issue resolved an issue via an AJAX request.

    Add the issue to the Resolved Issues table. Issue ID is not currently preserved.
    '''
    issue = Issue.objects.get(id=issueno)
    res = ResolvedIssue.from_issue(issue)

    issue.delete()

    return HttpResponse('')


@login_required
def drop_issue(request, issueno):
    '''
    Route for dropping an issue via an AJAX request.
    '''
    issue = Issue.objects.get(id=issueno)
    request.user.issues_joined.remove(issue)
    request.user.save()

    return HttpResponse('')


@login_required
def search(request):
    '''
    GET route for handling the search bar request.
    '''
    if request.method != "GET":
        return redirect('/')

    searchstr = request.GET.get('nav-search').strip()
    print(searchstr)

    if searchstr == '':
        return redirect('/')

    searchstr = searchstr.split()
    catqueries = Q(name__icontains=searchstr[0])
    issuequeries = Q(desc__icontains=searchstr[0]) | Q(short__icontains=searchstr[0])
    for term in searchstr[1:]:
        catqueries = catqueries | Q(name__icontains=term)
        issuequeries = issuequeries | Q(desc__icontains=term) | Q(short__icontains=term)

    context = {
        'categories': Category.objects.filter(catqueries),
        'issues': Issue.objects.filter(issuequeries)
    }

    return render(request, 'issues/search.html', context)


def resolved(request):
    '''
    Route for displaying resolved issues.
    '''
    context = {
        'issues': ResolvedIssue.objects.all()
    }
    return render(request, 'issues/resolved.html', context)
