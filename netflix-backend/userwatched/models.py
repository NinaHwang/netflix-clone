from django.db import models

from user.models import SubUser
from movie.models import Movie, Series

# Create your models here.

class UserWatched(models.Model):
    movie = models.ForeignKey(
        Movie,
        null=True,
        on_delete=models.CASCADE
    )
    series = models.ForeignKey(
        SeriesVideo,
        null=True,
        on_delete=models.CASCADE
    )
    subuser = models.ForeignKey(SubUser, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now=True)
    save_time = models.DurationField(null=True)

    class Meta:
        db_table = 'watched_movies'
