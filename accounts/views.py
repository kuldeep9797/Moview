from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages

from movie.options import genre_choices, year_choices
from .models import WatchList, FavoriteList, Profile, FriendShip
from movie.models import Gerne


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

    context = {
        "favorite_movies" : favorite_movies,
        "watched_movies" : watched_movies,
        "your_friends": your_friends,
        "friend_count": friend_count,
        'genre_choices': genre_choices,
    }
    return render(request, 'dashboard/dashboard.html', context)


def user_profile(request, user_id):
    print(user_id)
    return redirect('index')