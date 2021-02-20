from django.shortcuts import render

def login(request):
    return render(request, 'login_page/login.html')

def register(request):
    return render(request, 'register_page/register.html')

def login_process(request):
    # TODO All login logic here (Darsh, Shruti)
    return render(request, 'index.html')

def register_process(request):
    # TODO All register logic here (Darsh, Shruti)
    return render(request, 'index.html')
