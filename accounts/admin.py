from django.contrib import admin
from .models import FavoriteList, WatchList

# Register your models here.
@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_per_page = 25

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_per_page = 25