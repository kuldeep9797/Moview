from django.urls import path

from . import views

urlpatterns = [
    path('<int:movie_id>', views.movie, name='movie'),
    path('add_review', views.add_review, name='add_review'),
]