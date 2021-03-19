from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Movie, Review
from .options import genre_choices, year_choices
from accounts.models import WatchList, FavoriteList, Profile, FriendShip, Notification
from accounts.templatetags.profile_data import get_profile_image, get_profile_name, get_profile_genre

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

        your_friends = None
        if (request.user.is_authenticated):
            your_friends = FriendShip.objects.filter(user1=request.user)

        user_with_movie = []
        if (request.user.is_authenticated):
            for friend in FriendShip.objects.filter(user1=request.user):
                if (FavoriteList.objects.filter(user=friend.user2.id, movie_id=movie).exists()):
                    user_with_movie.append(friend.user2.id)

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
            'your_friends': your_friends,
            'user_with_movie': user_with_movie,
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
        review.rating = rating
        review.comment = review_text
        review.save()
        # Message
        messages.success(request, 'Your review updated successfully.')
    else:
        new_review = Review(user = user_db, rating = rating, comment=review_text, movie_id = movie_db)
        new_review.save()
        # Message
        messages.success(request, 'Your review added successfully.')
    
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


# Suggest movie to friend
# -------------------------------------------------------
def suggest_movie(request):
    if (request.user.is_authenticated):
        movie_id = Movie.objects.get(id=request.POST.get('movie_id'))
        user_id_to = User.objects.get(id=request.POST.get('friend'))
        user_id_from = request.user

        if (Notification.objects.filter(movie_id = movie_id, user1 = user_id_from, user2 = user_id_to).exists()):
            messages.error(request, 'You already suggested this movie to this user')
        else:
            movie_genre = movie_id.gerne_ids.all()
            movie_genres = []
            for genre in movie_genre:
                movie_genres.append(genre.name)
            
            user_to_genres = get_profile_genre(user_id=user_id_to.id)

            print("Friend's genres", user_to_genres)
            print("Movie's genres", movie_genres)
            # ['action', 'adventure', 'animation', 'crime', 'horror', 'sci-fi', 'mystery']

            add_notification_flag = False
            for genre in movie_genres:
                if (genre in user_to_genres):
                    add_notification_flag = True

            if (add_notification_flag):
                notification = Notification(movie_id = movie_id, user1 = user_id_from, user2 = user_id_to)
                notification.save();
                messages.success(request, 'Suggested successfully.')
            else:
                messages.error(request, "Your friend usualy doesn't like movies with this type of genre.")

    return redirect('movie', movie_id = request.POST.get('movie_id'))



# browse home page
# -------------------------------------------------------
def browse(request):
    movies = Movie.objects.all()

    trending_movies = movies.filter(isTrending = True)[:6]
    upcoming_movies = movies.filter(isUpcoming = True)[:6]
    theater_movies = movies.filter(isInTheater = True)[:6]

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
    movies = movies.filter(isTrending = True)

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
    movies = movies.filter(isUpcoming = True)

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
    movies = movies.filter(isInTheater = True)

    theater_movies = movies

    context = {
        'genre_choices': genre_choices,
        'year_choices': year_choices,
        'trending_movies': theater_movies,
    }
    return render(request, 'movie_list/theater_movie_list.html', context)