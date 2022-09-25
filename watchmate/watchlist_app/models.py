
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

"""class Movie  (models.Model):
    name=models.CharField(max_length=250)
    description=models.CharField(max_length=150)
    activate=models.BooleanField(default=True)

    def __str__(self) :
        return self.name
        """



class StreamPlataform(models.Model):
    name=models.CharField(max_length=30)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=300)
    def __str__(self) :
        return self.name


class WatchList(models.Model):
    title=models.CharField(max_length=150)
    storyline=models.CharField(max_length=200)
    activate=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    plataform=models.ForeignKey(StreamPlataform,on_delete=models.CASCADE,related_name="watchlist")
    def __str__(self) :
        return self.title

class Review (models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=1)
    description=models.CharField(max_length=200,null=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return str(self.rating)