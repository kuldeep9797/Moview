from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
from django.db.models import Avg


# *MOVIE TABLE
# *movie_id (int)  - I think this is the automatically generated with django so no need to add in the model class
# *movie_title (string)
# *movie_poster (image)
# *movie_coverphoto (image)
# *movie_discription (string)
# *rating (int between 1 to 5)  - this will be the average rating from all user
# *movie release year (int)
# *movie genre (many to many relation)
# *__str__ will be the movie title
class Movie(models.Model):
    def current_year():
        return datetime.date.today().year

    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='poster/%Y/%m/%d/')
    cover_photo = models.ImageField(upload_to='cover_photo/%Y/%m/%d/')
    description = models.TextField(blank=True)
    # avg_rating = models.FloatField(blank=True)
    release_year = models.IntegerField('year', choices=[(r,r) for r in range(1900, datetime.date.today().year+3)], default=current_year)
    gerne_ids = models.ManyToManyField('Gerne',blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.FloatField()
    comment = models.TextField()
    movie_id = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)  
    def __str__(self):
        return self.user.username + "/" + self.movie_id.name

#     @classmethod
#     def post_create(cls, sender, instance, created, *args, **kwargs):
#         if created:
#             current
#             self.movie_id.average_rating = 
#         # ...what needs to happen on create

# post_save.connect(Review.post_create, sender=MyModel)

class Gerne(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
