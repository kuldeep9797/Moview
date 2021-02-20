from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    # TODO link to about page when done (Bhardvaj)
    return render(request, 'index.html')
