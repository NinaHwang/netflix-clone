from django.db import models

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=200)
    is_service = models.BooleanField()
    service_date = models.DateField(null=True, auto_now=False)
    poster1 = models.CharField(max_length=500)
    poster2 = models.CharField(max_length=500, null=True)
    description = models.TextField()
    age = models.IntegerField()
    recommended = models.IntegerField()
    released = models.DateField(auto_now=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Movie(Video):
    duration = models.DurationField()
    preview = models.CharField(max_length=500)
    link = models.CharField(max_length=500)


    class Meta:
        db_table = 'movies'


class Series(Video):
   class Meta:
       db_table = 'serieses'


class SeriesVideo(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    season = models.IntegerField()
    episode = models.IntegerField()
    name = models.CharField(max_length=200, null=True)
    duration = models.DurationField()
    preview = models.CharField(max_length=500)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'series_videos'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'


class MovieTag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.movie.name}-{self.tag.name}'

    class Meta:
        db_table = 'movie_tags'


class SeriesTag(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.series.name}-{self.tag.name}'

    class Meta:
        db_table = 'series_tags'



class Producer(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'actors'


class MovieProducer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    is_actor = models.BooleanField()

    def __str__(self):
        return f'{self.movie.name}-{self.producer.name}'

    class Meta:
        db_table = 'movie_producers'


class SeriesProducer(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    is_actor = models.BooleanField()

    def __str__(self):
        return f'{self.series.name}-{self.producer.name}'

    class Meta:
        db_table = 'series_producers'

