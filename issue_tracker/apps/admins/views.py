from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.issues.models import Issue, ResolvedIssue
from apps.users.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest

# Route for testing the template.
# def template(request):
#     return render(request, 'admins/template.html')

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
        'resolvedissues': ResolvedIssue.objects.all().order_by('-created_on')[0:9],
    }

    return render(request, 'admins/admin.html', context)


@require_adminpage
def add_user_to_issue(request, issueno):
    '''
    AJAX POST route for admins to add an issue to a user's watch list.

    -> Partial with HTML for the admin table.
    '''
    if request.method != 'POST':
        messages.error('Request type was not POST.')
        return redirect(admin_home)

    if not request.user.permissions.adminpage:
        messages.error('User lacks privleges to make this request.')
        return redirect('/')

    try:
        issue = Issue.objects.get(id=issueno)
    except ObjectDoesNotExist:
        messages.error('This issue no longer exists.')
        return redirect(admin_home)

    for id in request.POST.get('ids').split():
        try:
            issue.users.add(User.objects.get(id=int(id)))
        except ObjectDoesNotExist:
            pass

    issue.save()

    context = {
        'issue': issue
    }

    return render(request, 'admins/partials/users-td.html', context=context)


@require_adminpage
def edit(request, issueno):
    '''
    Handles multiple AJAX routes for the administration site based on the post data.

    -> HTML Partial to insert into the page.
    '''

    if not request.user.permissions.adminpage:
        return HttpResponseBadRequest()

    partial_templates = {
            'sev': 'admins/partials/sev-td.html',
            }

    try:
        issue = Issue.objects.get(id=issueno)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest()

    partial = None
    for key in request.GET.keys():
        if key in partial_templates:
            partial = partial_templates[key]
            break

    if partial is None or issue is None:
        return HttpResponseBadRequest()

    if 'sev' in request.GET:
        if 1 <= int(request.GET['sev']) <= 5:
            issue.priority = request.GET['sev']
            issue.save()
        else:
            return HttpResponseBadRequest()

    return render(request, partial, {'issue': issue})


@require_adminpage
def set_issue_owner(request, issueno):
    return HttpResponseBadRequest()
