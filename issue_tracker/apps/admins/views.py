from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.issues.models import Issue, ResolvedIssue
from apps.users.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# Route for testing the template.
# def template(request):
#     return render(request, 'admins/template.html')


@login_required
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


@login_required
def add_user_to_issue(request, issueno):
    '''
    AJAX POST route for admins to add an issue to a user's watch list.

    -> Partial with 
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