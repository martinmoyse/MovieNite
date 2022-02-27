from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

class User(AbstractUser):
    pass

class List(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    listId = models.CharField(max_length=6, blank=False)
    date = models.DateTimeField(auto_now_add=True)

class ListedShow(models.Model):
    userOwner = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    listOwner = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    imdbId = models.CharField(max_length=15, blank=False)
    title = models.CharField(max_length=300, blank=False)
    imdbRating = models.CharField(max_length=4)
    year = models.CharField(max_length=50)
    image = models.CharField(max_length=300)
