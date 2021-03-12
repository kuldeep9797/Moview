from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Avg
from django.contrib.auth.models import User

from .models import Movie, Review
from .options import genre_choices, year_choices
from accounts.models import WatchList, FavoriteList

# movie page data
# -------------------------------------------------------
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
        
        watch_listed = False
        if (request.user.is_authenticated):
            if (WatchList.objects.filter(user=request.user, movie_id=movie).exists()):
                watch_listed = True
            else:
                watch_listed = False

        favorited = False
        if (request.user.is_authenticated):
            if (FavoriteList.objects.filter(user=request.user, movie_id=movie).exists()):
                favorited = True
            else:
                favorited = False

        context = {
            'movie': movie,
            'reviews': reviews,
            'rating_avg': round(avg_rating['rating__avg'], 1),
            'review_count': reviews.count(),
            'watch_listed': watch_listed,
            'favorited': favorited,
            'user_review': user_review[0],
            'user_given_review': user_given_review,
            'genre_choices': genre_choices,
        }
    except Movie.DoesNotExist:
        raise Http404('Movie not found')
    return render(request, 'movie_page/movie_page.html', context)


# add_review method
# -------------------------------------------------------
def add_review(request):
    movie = request.POST.get('movie_id')
    user_id = request.user.id
    rating = request.POST.get('rating')
    review_text = request.POST.get('review')

    # Getting movie and user
    movie_db = Movie.objects.get(id=movie)
    user_db = User.objects.get(id=user_id)

    if (Review.objects.filter(movie_id = movie, user = user_id).exists()):
        review = Review.objects.get(movie_id = movie, user = user_id)
        print("Review Exists: " ,review)
        review.rating = rating
        review.comment = review_text
        review.save()
    else:
        new_review = Review(user = user_db, rating = rating, comment=review_text, movie_id = movie_db)
        new_review.save()
    
    return redirect('movie', movie_id = request.POST.get('movie_id'))


# Watched list add/remove
# -------------------------------------------------------
def add_remove_watch(request):
    movie = request.POST.get('movie_id')
    user_id = request.user.id

    movie_db = Movie.objects.get(id=movie)
    user_db = User.objects.get(id=user_id)

    print("Add to watched list")

    if (WatchList.objects.filter(movie_id = movie, user = user_id).exists()):
        WatchList.objects.filter(movie_id = movie, user = user_id).delete()
    else:
        new_addition = WatchList(user = user_db, movie_id = movie_db)
        new_addition.save()
    
    return redirect('movie', movie_id = request.POST.get('movie_id'))


# Favorite list add/remove
# -------------------------------------------------------
def add_remove_favorite(request):
    movie = request.POST.get('movie_id')
    user_id = request.user.id

    movie_db = Movie.objects.get(id=movie)
    user_db = User.objects.get(id=user_id)

    print("Add to favorite list")

    if (FavoriteList.objects.filter(movie_id = movie, user = user_id).exists()):
        FavoriteList.objects.filter(movie_id = movie, user = user_id).delete()
    else:
        new_addition = FavoriteList(user = user_db, movie_id = movie_db)
        new_addition.save()
    # Add logic
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


# search result data
#-------------------------------------------------------
def browse_result(request):
    movies = Movie.objects.all()

    if (movies.count() == 0):
        has_results = False
    else:
        has_results = True

    # Name
    if 'name' in request.GET:
        name = request.GET['name']
        if name:
            movies = movies.filter(name__icontains=name)

    # Year
    if 'years' in request.GET:
        year = request.GET['years']
        if year:
            movies = movies.filter(release_year =year)

    # genres
    if 'genres' in request.GET:
        genre = request.GET['genres']
        # print(genre)
        if genre:
            filtered_movies = []
            for movie in movies:
                id, gernes = movie.id,movie.gerne_ids.all()
                for rec in gernes:
                    print(id)
                    print(rec.name)
                    print(genre)
                    if rec.name.lower() == genre:
                        filtered_movies.append(id)
            movies = movies.filter(pk__in=filtered_movies)
            print(filtered_movies)

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'has_results': has_results,
        'movies': movies,
        'get_request': request.GET,
    }
    return render(request, 'browse_page/browse_result.html', context)


# Tranding movie list page
#-------------------------------------------------------
def trending_movie_list(request):
    movies = Movie.objects.all()

    trending_movies = movies

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'trending_movies': trending_movies,
    }
    return render(request, 'movie_list/trending_movie_list.html', context)


# Upcoming movie list page
#-------------------------------------------------------
def upcoming_movie_list(request):
    movies = Movie.objects.all()

    upcoming_movies = movies

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'trending_movies': upcoming_movies,
    }
    return render(request, 'movie_list/upcoming_movie_list.html', context)


# Theater movie list page
#-------------------------------------------------------
def theater_movie_list(request):
    movies = Movie.objects.all()

    theater_movies = movies

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'trending_movies': theater_movies,
    }
    return render(request, 'movie_list/theater_movie_list.html', context)