from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('login_process', views.login_process, name='login_process'),
    path('register_process', views.register_process, name='register_process'),
    path('logout_process', views.logout_process, name='logout_process'),
    path('profile_setup', views.profile_setup, name='profile_setup'),
    path('profile_setup_process', views.profile_setup_process, name='profile_setup_process'),
    path('profile_update_process', views.profile_update_process, name='profile_update_process'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('favorite_movie_list', views.favorite_movie_list, name='favorite_movie_list'),
    path('watch_movie_list', views.watch_movie_list, name='watch_movie_list'),
    path('<int:user_id>', views.user_profile, name='user_profile'),
    path('user_favorite_movie_list/<int:user_id>', views.user_favorite_movie_list, name='user_favorite_movie_list'),
    path('user_watch_movie_list/<int:user_id>', views.user_watch_movie_list, name='user_watch_movie_list'),
    path('send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('movie_notification_handler', views.movie_notification_handler, name='movie_notification_handler'),
    path('friend_request_notification_handler', views.friend_request_notification_handler, name='friend_request_notification_handler'),
    path('user_list', views.user_list, name='user_list'),
    path('movie_request', views.movie_request, name='movie_request'),
]