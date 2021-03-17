from django.urls import path

from . import views

urlpatterns = [
    path('', views.browse, name='browse'),
    path('results', views.browse_result, name='browse_result'),
    path('<int:movie_id>', views.movie, name='movie'),
    path('add_review', views.add_review, name='add_review'),
    path('add_remove_watch', views.add_remove_watch, name='add_remove_watch'),
    path('add_remove_favorite', views.add_remove_favorite, name='add_remove_favorite'),
    path('trending_movie_list', views.trending_movie_list, name='trending_movie_list'),
    path('upcoming_movie_list', views.upcoming_movie_list, name='upcoming_movie_list'),
    path('theater_movie_list', views.theater_movie_list, name='theater_movie_list'),
    path('suggest_movie', views.suggest_movie, name='suggest_movie'),
]