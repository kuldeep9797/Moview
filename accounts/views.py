from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

def login(request):
    if (request.user.is_authenticated):
        return redirect('index')
    return render(request, 'login_page/login.html')

def register(request):
    if (request.user.is_authenticated):
        return redirect('index')
    return render(request, 'register_page/register.html')

def login_process(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print("user is:",username, password, user)
        if user is not None:
            auth.login(request, user)
            print('You are now logged in')
            return redirect('index')
        else:
            print('Invalid credentials')
            return redirect('login')
    else:
        return redirect('login')

def register_process(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print("request is POST:" , username, password, email)
        if User.objects.filter(username=username).exists():
                print('That username is taken')
                return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                print('That email is being used')
                return redirect('register')
            else:
                # Looks good
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                )
                user.save()
                print('You are now registerd and can log in')
                return redirect('login')

    else:
        return redirect('register')

def logout_process(request):
    if request.method == 'POST':
        auth.logout(request)
        print('You are now logged out')
        return redirect('login')

