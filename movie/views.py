from django.shortcuts import render, redirect
from .models import Movie, Review
from django.http import Http404
from django.db.models import Avg

from .options import genre_choices, year_choices


def movie(request, movie_id):
    # *lsit of user who are friend with the user, who logged in, and have this movie in favorite list
    try:
        movie = Movie.objects.get(id=movie_id)
        reviews = Review.objects.filter(movie_id=movie_id)
        avg_rating = Review.objects.filter(movie_id=movie_id).aggregate(Avg("rating"))
        if (reviews.count() == 0):
            avg_rating = {'rating__avg': 0}
        user_review = ['None']
        user_given_review = False
        if (request.user.is_authenticated):
            user_review = Review.objects.filter(user=request.user, movie_id=movie_id)
            if (user_review.count() == 0):
                user_given_review = False
                user_review = ['None']
            else:
                user_given_review = True

        context = {
            'movie': movie,
            'reviews': reviews,
            'rating_avg': avg_rating['rating__avg'],
            'review_count': reviews.count(),
            'watch_listed': False,
            'favorited': False,
            'user_review': user_review[0],
            'user_given_review': user_given_review,
        }
    except Movie.DoesNotExist:
        raise Http404('Movie not found')
    return render(request, 'movie_page/movie_page.html', context)


# TODO Add logic for the add_review method
# TODO-------------------------------------------------------
def add_review(request):
    # If the review from the user exist then update it
    # Otherwise create the new review entry
    # Movie id is in the post request so you can access it with 'request.POST.get('movie_id')' and user is logged in

    return redirect('movie', movie_id = request.POST.get('movie_id'))


# TODO data for browse page
# TODO-------------------------------------------------------
def browse(request):
    movies = Movie.objects.all()

    trending_movies = movies
    upcoming_movies = movies
    theater_movies = movies

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'trending_movies': trending_movies,
        'upcoming_movies': upcoming_movies,
        'theater_movies': theater_movies,
    }
    return render(request, 'browse_page/browse_page.html', context)


# TODO search result data
# TODO-------------------------------------------------------
def browse_result(request):
    movies = Movie.objects.all()

    if (movies.count() == 0):
        has_results = False
    else:
        has_results = True

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'has_results': has_results,
        'movies': movies,
        'get_request': request.GET,
    }
    return render(request, 'browse_page/browse_result.html', context)
