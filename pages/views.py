from django.shortcuts import render, redirect
from django.contrib import messages

from movie.models import Movie

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    trending_movies = movies.filter(isTrending = True)[:6]

    context = {
        'trending_movies': trending_movies
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')
