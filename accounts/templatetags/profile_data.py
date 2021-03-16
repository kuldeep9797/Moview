from django import template
from movie.models import Movie, Review
from accounts.models import Profile, FavoriteList, WatchList
from django.db.models import Avg

register = template.Library()


@register.simple_tag
def get_profile_image(user_id):
    profile = Profile.objects.filter(user_id=user_id)
    profile_photo = profile[0].profile_photo.url
    return profile_photo


@register.simple_tag
def get_profile_name(user_id):
    profile = Profile.objects.filter(user_id=user_id)
    profile_name = profile[0].first_name + " " + profile[0].last_name
    return profile_name

@register.simple_tag
def get_profile_genre(user_id):
    profile = Profile.objects.filter(user_id=user_id)
    genres = profile[0].favorite_genre.all()
    profile_genre = []
    for genre in genres:
        profile_genre.append(genre.name)
    return profile_genre


register.simple_tag(get_profile_genre)
register.simple_tag(get_profile_image)
register.simple_tag(get_profile_name)