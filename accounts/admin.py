from django.contrib import admin
from .models import FavoriteList, WatchList

# Register your models here.
@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'user']
    search_fields = ('movie_id', 'user')
    list_per_page = 25

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'user']
    search_fields = ('movie_id', 'user')
    list_per_page = 25