from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    # TODO link to about page when about page is done (Bhardvaj)
    return redirect('index')
