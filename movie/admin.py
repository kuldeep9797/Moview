from django.contrib import admin
from .models import Movie, Review
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_year']
    search_fields = ('name',)
    list_per_page = 25

@admin.register(Review)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'user', 'rating']
    search_fields = ('user','movie_id')
    list_per_page = 25
