from django.shortcuts import render, redirect
from .models import Movie, Review
from django.http import Http404
from django.db.models import Avg


def movie(request, movie_id):
    # *review from the review table where user is who logged in
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
            else:
                user_given_review = True

        print(user_review)

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


def add_review(request):
    return redirect('movie', movie_id = request.POST.get('movie_id'))
