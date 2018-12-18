from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User, RegKey


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/issues/all')
    return render(request, 'users/login_and_reg.html')


def register_submit(request):
    '''Handles the POST request for the registration form.'''
    if request.method != "POST":
        return redirect(login)

    new_user = User.objects.create_user(username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
    new_user = authenticate(request, username=new_user.username, password=new_user.password)
    if new_user is not None:
        login(request, new_user)
    else:
        return redirect(login)

    return redirect('/issues/all')


def login_submit(request):
    '''Handles the POST request for the login form.'''
    if request.method != "POST":
        return redirect(login)

    new_user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
    if new_user is not None:
        login(request, new_user)
    else:
        redirect(login)
    return redirect('/issues/all')
