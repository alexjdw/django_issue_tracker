from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def template(request):
    return render(request, 'admins/template.html')


@login_required
def admin_home(request):
    # if not request.user.is_superuser:
    #     return redirect('/issues/all')
    return render(request, 'admins/admin.html')
