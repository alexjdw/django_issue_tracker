from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from apps.issues.models import Issue, ResolvedIssue
from apps.users.models import User
from apps.lib.decorators import get_issue_from_issueno


def require_adminpage(func):
    '''
    Decorator for requiring the user.permissions.adminpage permission.
    Includes @login_required as login is required to check permissions.

    -> Function as is but now requiring login and correct permission.
    '''
    @login_required
    def decorated(*args, **kwargs):
        request = args[0]
        if not request.user.permissions.adminpage:
            return HttpResponseBadRequest("User is not an supervisor.")
        return func(*args, **kwargs)

    return decorated


@require_adminpage
def admin_home(request):
    '''
    Home page for issue administrators.
    '''
    if not request.user.permissions.adminpage:
        return redirect('/issues/all')

    context = {
        'issues': Issue.objects.all(),
        'resolvedissues': 
            ResolvedIssue.objects.all().order_by('-created_on')[0:9],
    }

    return render(request, 'admins/admin.html', context)


@require_adminpage
@get_issue_from_issueno
def add_user_to_issue(request, issue):
    '''
    AJAX POST route for admins to add an issue to a user's watch list.

    -> Partial with HTML for the admin table.
    '''

    for id in request.GET.get('ids').split():
        try:
            issue.users.add(User.objects.get(id=int(id)))
        except ObjectDoesNotExist:
            # Someone submitted an invalid user ID.
            messages.error("An invalid user ID was sumbitted, so not all "
                           + "of the requested users were added.")

    issue.save()

    return render(request, 'admins/partials/users-td.html',  {'issue': issue})


@require_adminpage
@get_issue_from_issueno
def edit_priority(request, issue):
    '''
    Edits the priority of an issue.

    -> HTML Partial to insert into the page.
    '''

    if not request.user.permissions.adminpage:
        return HttpResponseBadRequest()

    print(request.GET)
    partial = 'admins/partials/sev-td.html'

    if 'sev' in request.GET:
        if 1 <= int(request.GET['sev']) <= 5:
            issue.priority = request.GET['sev']
            issue.save()
        else:
            return HttpResponseBadRequest()

    return render(request, partial, {'issue': issue})


@require_adminpage
@get_issue_from_issueno
def set_owner(request, issue):
    '''
    AJAX GET route for updating an issue's owner id.
    '''
    partial = 'admins/partials/owner-td.html'
    owner_id = request.GET.get('ids').strip()
    try:
        issue.owner = User.objects.get(id=owner_id)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Owner does not exist: ", owner_id)

    issue.save()
    return render(request, partial, {issue: issue})
