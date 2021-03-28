from django.contrib import admin
from .models import Movie, Review, Gerne, MovieRequest
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_year', 'isTrending', 'isUpcoming', 'isInTheater']
    search_fields = ('name',)
    list_filter = ('gerne_ids',)
    list_editable = ('isTrending', 'isUpcoming', 'isInTheater')
    list_per_page = 25

@admin.register(Review)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'user', 'rating']
    search_fields = ('user','movie_id')
    list_filter = ('rating',)
    list_per_page = 25

@admin.register(Gerne)
class GerneAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ('name',)
    list_per_page = 25

@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    list_display = ['__str__',]
    search_fields = ('user_id','movieName')
    list_filter = ('release_year',)
    list_per_page = 25

