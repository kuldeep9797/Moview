from django.contrib import admin
from .models import FavoriteList, WatchList, Profile, FriendShip, Notification

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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user_id']
    search_fields = ('first_name', 'user_id', 'last_name')
    list_filter = ('favorite_genre',)
    list_per_page = 25

@admin.register(FriendShip)
class FriendShipAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user1', 'user2']
    search_fields = ('user1', 'user2')
    list_per_page = 25

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date']
    search_fields = ('user1', 'user2')
    list_filter = ('request_type',)
    list_per_page = 25