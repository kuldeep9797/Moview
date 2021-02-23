from django.db import models

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


# *REVIEW TABLE
# *rating_id (int)  - I think this is the automatically generated with django so no need add in the model class
# *movie_id (int)
# *user_id (int)
# *rating (int between 1 to 5)  - this will be user specific rating
# *comment (string)
