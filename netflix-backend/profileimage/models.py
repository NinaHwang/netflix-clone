from django.db import models

# Create your models here.

class ImageCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'image_categories'


class ProfileImage(models.Model):
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=300)

    class Meta:
        db_table = 'profile_images'
