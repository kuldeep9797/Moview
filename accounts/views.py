from django.shortcuts import render, redirect

def login(request):
    return render(request, 'login_page/login.html')

def register(request):
    return render(request, 'register_page/register.html')

def login_process(request):
    # TODO login logic here (Darsh, Shruti)
    return redirect('index')

def register_process(request):
    # TODO Register logic here (Darsh, Shruti)
    return redirect('index')

def logout_process(request):
    # TODO All logic for Logout here (Darsh, Shruti)
    return redirect('index')
