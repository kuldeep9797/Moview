from django import template
from movie.models import Movie, Review
from django.db.models import Avg

register = template.Library()


@register.simple_tag
def avg_movie_rating(movie_id):
    reviews = Review.objects.filter(movie_id=movie_id)

    avg_rating = Review.objects.filter(movie_id=movie_id).aggregate(Avg("rating"))
    if (reviews.count() == 0):
        avg_rating = {'rating__avg': 0}
    else:
        avg_rating = round(avg_rating['rating__avg'], 1)

    return avg_rating

register.simple_tag(avg_movie_rating)