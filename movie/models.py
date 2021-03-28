from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
from django.db.models import Avg


class Movie(models.Model):
    def current_year():
        return datetime.date.today().year

    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='poster/%Y/%m/%d/')
    cover_photo = models.ImageField(upload_to='cover_photo/%Y/%m/%d/')
    description = models.TextField(blank=True)
    release_year = models.IntegerField('year', choices=[(r,r) for r in range(1900, datetime.date.today().year+3)], default=current_year)
    gerne_ids = models.ManyToManyField('Gerne',blank=True)
    isTrending = models.BooleanField(default = False)
    isUpcoming = models.BooleanField(default = False)
    isInTheater = models.BooleanField(default = False)

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.FloatField()
    comment = models.TextField()
    movie_id = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.user.username + "/" + self.movie_id.name


class Gerne(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MovieRequest(models.Model):
    movieName = models.CharField(max_length=200)
    release_year = models.IntegerField()
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username + " reqested '" + self.movieName + "' movie"
