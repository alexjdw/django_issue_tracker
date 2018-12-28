from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.issues.models import Issue, ResolvedIssue


def template(request):
    return render(request, 'admins/template.html')


@login_required
def admin_home(request):
    if not request.user.permissions.adminpage:
        return redirect('/issues/all')
    
    context = {
        'issues': Issue.objects.all(),
        'resolvedissues': ResolvedIssue.objects.all().order_by('-created_on')[0:9],
    }

    return render(request, 'admins/admin.html', context)
