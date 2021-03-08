from django.db import models

from profileimage.models import ProfileImage
# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=10)
    subuser_cnt = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'memberships'


class User(models.Model):
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=300)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    is_agreed = models.BooleanField(default=True)
    is_agreed_marketing = models.BooleanField()
    viewer_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class SubUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    image = models.ForeignKey(
        ProfileImage,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subusers'


