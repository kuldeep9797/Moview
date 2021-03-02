from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

# Create your models here.
class WatchList(models.Model):
    movie_id = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + "/" + self.movie_id.name

class FavoriteList(models.Model):
    movie_id = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + "/" + self.movie_id.name
