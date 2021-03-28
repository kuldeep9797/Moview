from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

from movie.options import genre_choices, year_choices
from .models import WatchList, FavoriteList, Profile, FriendShip, Notification
from movie.models import Gerne, MovieRequest
from accounts.templatetags.profile_data import get_profile_image, get_profile_name, get_profile_genre


# Login page
#-------------------------------------------------------
def login(request):
    if (request.user.is_authenticated):
        if (Profile.objects.filter(user_id=request.user).exists()):
            return redirect('dashboard')
        else:
            return redirect('profile_setup')
    return render(request, 'login_page/login.html')


# Register page
#-------------------------------------------------------
def register(request):
    if (request.user.is_authenticated):
        if (Profile.objects.filter(user_id=request.user).exists()):
            return redirect('dashboard')
        else:
            return redirect('profile_setup')
    return render(request, 'register_page/register.html')


# Profile setup page
#-------------------------------------------------------
def profile_setup(request):
    if request.user.is_authenticated:
        if (Profile.objects.filter(user_id=request.user).exists()):
                return redirect('dashboard')
    context = {
        'genre_choices': genre_choices,
    }
    return render(request, 'profile_setup/profile_setup.html', context)


# Login process logic
#-------------------------------------------------------
def login_process(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print("user is:",username, password, user)
        if user is not None:
            auth.login(request, user)
            print('You are now logged in')
            # Message
            messages.success(request, 'You are now logged in.')
            if (Profile.objects.filter(user_id=user).exists()):
                return redirect('dashboard')
            else:
                return redirect('profile_setup')
        else:
            print('Invalid credentials')
            # Message
            messages.error(request, 'Invalid credentials.');
            return redirect('login')
    else:
        return redirect('login')


# Register process logic
#-------------------------------------------------------
def register_process(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print("request is POST:" , username, password, email)
        if User.objects.filter(username=username).exists():
                print('That username is taken')
                # Message
                messages.error(request, 'That username is already taken');
                return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                print('That email is being used')
                # Message
                messages.error(request, 'That Email is already used');
                return redirect('register')
            else:
                # Looks good
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                )
                user.save()
                print('You are now registerd and can log in')
                # Message
                messages.success(request, 'You are now registerd and can login.')
                return redirect('login')

    else:
        return redirect('register')


# Logout process logic
#-------------------------------------------------------
def logout_process(request):
    if request.method == 'POST':
        auth.logout(request)
        print('You are now logged out')
        # Message
        messages.success(request, 'You are now logged out.')
        return redirect('login')


# Profile setup process logic
#-------------------------------------------------------
def profile_setup_process(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            userId = request.user.id
            user_db = User.objects.get(id=userId)
            firstName = request.POST.get('firstname')
            lastName = request.POST.get('lastname')
            myfile = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
            genres = request.POST.getlist('genre')
            favorite_genre = []
            for genre in genres:
                favorite_genre.append(Gerne.objects.get(name=genre))

            new_profile = Profile(first_name=firstName, last_name=lastName, user_id=user_db, profile_photo=myfile)
            new_profile.save()
            new_profile.favorite_genre.add(*favorite_genre)
            new_profile.save()
    # Message
    messages.success(request, 'Your profile updated successfully.')
    return redirect('dashboard')


# Profile setup process logic
#-------------------------------------------------------
def profile_update_process(request):
    if request.method == 'POST' and request.user.is_authenticated:
        profile = Profile.objects.get(user_id=request.user.id)

        # Update Firstname and lastname
        firstName = request.POST.get('firstname')
        lastName = request.POST.get('lastname')
        profile.first_name = firstName
        profile.last_name = lastName
        profile.save()

        # Update profile image
        myfile = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
        if (myfile):
            profile.profile_photo = myfile
            profile.save()
        
        # Update favorite genres
        genres = request.POST.getlist('genre')
        favorite_genre = []
        for genre in genres:
            favorite_genre.append(Gerne.objects.get(name=genre))
        profile.favorite_genre.clear()
        profile.favorite_genre.add(*favorite_genre)
        profile.save()

    #Messages
    messages.success(request, 'Your profile updated successfully.')
    return redirect('dashboard')


# Dashboard page
# -----------------------------------------------------
def dashboard(request):
    if (not request.user.is_authenticated):
        return redirect('login')
    else:
        if ( not Profile.objects.filter(user_id=request.user).exists()):
            return redirect('profile_setup')

    user_id = request.user

    favorite_movies = FavoriteList.objects.filter(user = user_id)[:4]
    watched_movies = WatchList.objects.filter(user = user_id)[:4]

    your_friends = FriendShip.objects.filter(user1=user_id)
    friend_count = FriendShip.objects.filter(user1=user_id).count()

    notification = Notification.objects.filter(user2=user_id).order_by('-date')

    profile = Profile.objects.get(user_id=request.user)

    context = {
        "favorite_movies" : favorite_movies,
        "watched_movies" : watched_movies,
        "your_friends": your_friends,
        "friend_count": friend_count,
        'genre_choices': genre_choices,
        "notification": notification,
        "profile": profile,
        "year_choices": year_choices,
    }
    return render(request, 'dashboard/dashboard.html', context)


# Users favorite movie
# -----------------------------------------------------
def favorite_movie_list(request):
    favorite_movies = FavoriteList.objects.filter(user = request.user)
    profile = Profile.objects.get(user_id=request.user)
    friend_count = FriendShip.objects.filter(user1=request.user).count()

    context = {
        "favorite_movies": favorite_movies,
        'genre_choices': genre_choices,
        "friend_count": friend_count,
    }

    return render(request, 'dashboard/favorite_list.html', context)


# Users watched movies
# -----------------------------------------------------
def watch_movie_list(request):
    watch_movies = WatchList.objects.filter(user = request.user)
    profile = Profile.objects.get(user_id=request.user)
    friend_count = FriendShip.objects.filter(user1=request.user).count()

    context = {
        "watch_movies": watch_movies,
        'genre_choices': genre_choices,
        "friend_count": friend_count,
    }

    return render(request, 'dashboard/watch_list.html', context)


# User page
# -----------------------------------------------------
def user_profile(request, user_id):
    if request.user.is_authenticated:
        if request.user.id == user_id:
            return redirect('dashboard')
        else:
            favorite_movies = FavoriteList.objects.filter(user = user_id)[:4]
            watched_movies = WatchList.objects.filter(user = user_id)[:4]

            friend_count = FriendShip.objects.filter(user1=user_id).count()
            favorite_count = FavoriteList.objects.filter(user = user_id).count()

            friends = FriendShip.objects.filter(user1=user_id)

            already_friend = False
            if (FriendShip.objects.filter(user1 = user_id, user2=request.user)):
                already_friend = True

            request_sent = False
            if (Notification.objects.filter(request_type=True, user1=request.user.id, user2=user_id)):
                request_sent = True

            context = {
                'favorite_movies' : favorite_movies,
                'watched_movies' : watched_movies,
                'friend_count' : friend_count,
                'favorite_count': favorite_count,
                'friends': friends,
                'user_id': user_id,
                'user': User.objects.get(id=user_id),
                'already_friend': already_friend,
                'request_sent': request_sent
            }

            return render(request, 'user_page/user_page.html', context)
    else:
        return redirect('login')


# Users favorite movie
# -----------------------------------------------------
def user_favorite_movie_list(request, user_id):
    favorite_movies = FavoriteList.objects.filter(user = user_id)
    friend_count = FriendShip.objects.filter(user1=user_id).count()
    favorite_count = FavoriteList.objects.filter(user = user_id).count()

    already_friend = False
    if (FriendShip.objects.filter(user1 = user_id, user2=request.user)):
        already_friend = True

    request_sent = False
    if (Notification.objects.filter(request_type=True, user1=request.user.id, user2=user_id)):
        request_sent = True

    context = {
        "favorite_movies": favorite_movies,
        'user_id': user_id,
        'user': User.objects.get(id=user_id),
        'friend_count' : friend_count,
        'favorite_count': favorite_count,
        'already_friend': already_friend,
        'request_sent': request_sent,
    }
    return render(request, 'user_page/user_favorite_list.html', context)


# Users watched movies
# -----------------------------------------------------
def user_watch_movie_list(request, user_id):
    watch_movies = WatchList.objects.filter(user = user_id)
    friend_count = FriendShip.objects.filter(user1=user_id).count()
    favorite_count = FavoriteList.objects.filter(user = user_id).count()

    already_friend = False
    if (FriendShip.objects.filter(user1 = user_id, user2=request.user)):
        already_friend = True

    request_sent = False
    if (Notification.objects.filter(request_type=True, user1=request.user.id, user2=user_id)):
        request_sent = True

    context = {
        "watch_movies": watch_movies,
        'user_id': user_id,
        'user': User.objects.get(id=user_id),
        'friend_count' : friend_count,
        'favorite_count': favorite_count,
        'already_friend': already_friend,
        'request_sent': request_sent,
    }
    return render(request, 'user_page/user_watch_list.html', context)


# send friend request process
# -----------------------------------------------------
def send_friend_request(request):
    if request.method == 'POST':
        if (request.user.is_authenticated):
            user_id = User.objects.filter(id=request.POST.get('user_id'))[0]
            user_logged_id = request.user
            if (FriendShip.objects.filter(user1=user_id, user2=user_logged_id)):
                FriendShip.objects.filter(user1=user_id, user2=user_logged_id).delete()
                FriendShip.objects.filter(user2=user_id, user1=user_logged_id).delete()
                messages.error(request, "You have unfriended " + User.objects.get(id=user_id.id).username)
            else:
                if (Notification.objects.filter(request_type=True, user1=user_logged_id, user2=user_id)):
                    messages.error(request, "You already sent friend request.")
                    return redirect('user_profile', user_id = request.POST.get('user_id'))
                else:
                    notification = Notification(request_type=True, user1=user_logged_id, user2=user_id)
                    notification.save()
        else:
            return redirect('login')
    return redirect('user_profile', user_id = request.POST.get('user_id'))


# Handle action for movie notification
# -----------------------------------------------------
def movie_notification_handler(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id');
        noti_id = request.POST.get('noti_id');

        notification = Notification.objects.get(id=noti_id)
        notification.is_read = True
        notification.save()
        return redirect('movie', movie_id = request.POST.get('movie_id'))
    else:
        return redirect('dashboard')


# handle action for friend notification
# -----------------------------------------------------
def friend_request_notification_handler(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id');
        noti_id = request.POST.get('noti_id');
        ad = request.POST.get('ad');

        if (ad == 'A'):
            print("Accept")
            notification = Notification.objects.get(id=noti_id)
            if (FriendShip.objects.filter(user1=user_id, user2=request.user.id)):
                pass
            else:
                friend = FriendShip(user1=User.objects.get(id=user_id), user2=request.user)
                friend.save()
                friend = FriendShip(user2=User.objects.get(id=user_id), user1=request.user)
                friend.save()
            notification.delete()
            messages.success(request, "You are now friends with " + User.objects.get(id=user_id).username)
        else:
            print("Decline")
            notification = Notification.objects.get(id=noti_id)
            notification.delete()
    return redirect('dashboard')


# Search User handler
# -----------------------------------------------------
def user_list(request):
    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST.get('name')
        data = []

        names = name.split()
        users = User.objects.all()

        for name in names:
            users_for_name = users.filter(username__icontains=name)

            for user in users_for_name:
                if (Profile.objects.filter(user_id=user.id).exists()):
                    user = {
                        'id': user.id,
                        'user_name': get_profile_name(user_id=user.id),
                        'user_photo_url': get_profile_image(user_id=user.id)
                    }
                    if (user in data) or (user['id'] == request.user.id):
                        print(name, "Already exits")
                    else:
                        print(name, "Added in data")
                        data.append(user)
                else:
                    print(name, "User don't have profile data")

        if (data):
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse("None", safe=False)
    else:
        return redirect('login')


# Movie request handler
# -----------------------------------------------------
def movie_request(request):
    if request.method == 'POST' and request.user.is_authenticated:
        movie_name = request.POST.get('moviename')
        release_year = request.POST.get('releaseyear')

        new_movie = MovieRequest(user_id=request.user, movieName=movie_name, release_year=release_year)
        new_movie.save()
        
        messages.success(request, "Movie request send successfully.")
        return redirect('dashboard')
    else:
        return redirect('login')
