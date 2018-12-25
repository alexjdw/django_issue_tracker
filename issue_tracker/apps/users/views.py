from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User, RegKey


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/issues/all')
    return render(request, 'users/login_and_reg.html')


def register_submit(request):
    '''Handles the POST request for the new user registration form.'''
    if request.method != "POST":
        return redirect(login_page)

    print(request.POST)
    new_user = User.objects.create_user(first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['email'],
                    email=request.POST['email'],
                    password=request.POST['password'])
    new_user = authenticate(request, username=new_user.username, password=request.POST['password'])
    if new_user is not None:
        login(request, new_user)
        return redirect('/issues/all')
    else:
        return redirect(login_page)


def login_submit(request):
    '''Handles the POST request for the new user login form.'''
    if request.method != "POST":
        return redirect(login_page)

    new_user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
    if new_user is not None:
        login(request, new_user)
    else:
        redirect(login_page)
    return redirect('/issues/all')
