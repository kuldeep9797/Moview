from django.shortcuts import render, redirect
from .models import Movie, Review
from django.http import Http404
from django.db.models import Avg


def movie(request, movie_id):

    # *movie form movie table
    # *is_in_favorite boolean value
    # *is_in_watched boolean value
    # *review from the review table where user is who logged in
    # *lsit of user who are friend with the user, who logged in, and have this movie in favorite list
    try:
        movie = Movie.objects.get(id=movie_id)
        reviews = Review.objects.filter(movie_id=movie_id)
        avg_rating = Review.objects.filter(movie_id=movie_id).aggregate(
            Avg("rating")
        )
        context = {
            'movie': movie,
            'reviews': reviews,
            'rating_avg': avg_rating,
        }
    except Movie.DoesNotExist:
        raise Http404('Movie not found')
    return render(request, 'movie_page/movie_page.html', context)
