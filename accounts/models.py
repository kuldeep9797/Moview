from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie, Gerne
from PIL import Image
from datetime import datetime

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

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photo/%Y/')
    favorite_genre = models.ManyToManyField('movie.Gerne',blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        im = Image.open(self.profile_photo)  
        width, height = im.size
        ratio = width / height

        N_height = 200
        N_width = int(N_height * ratio)
        im = im.resize((N_width, N_height))

        new_width = 200
        new_height = 200
        left = (N_width - new_width)/2
        top = (N_height - new_height)/2
        right = (N_width + new_width)/2
        bottom = (N_height + new_height)/2

        im = im.crop( (left, top, right, bottom) )
        im.save(self.profile_photo.path)

    def __str__(self):
        return self.first_name + " " + self.last_name;


class FriendShip(models.Model):
    user1 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_from')
    user2 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_to')

    def __str__(self):
        return self.user1.username + " friends with " + self.user2.username


class Notification(models.Model):
    request_type = models.BooleanField(default = False)
    is_read = models.BooleanField(default = False)
    user1 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='userNoti_from')
    user2 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='userNoti_to')
    movie_id = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='movie', null=True)
    date = models.DateTimeField(default = datetime.now, blank = False)

    def __str__(self):
        if self.request_type:
            return self.user1.username + " has sent friend request to " + self.user2.username
        else:
            return self.user1.username + " suggested " + self.movie_id.name + " movie to " + self.user2.username

