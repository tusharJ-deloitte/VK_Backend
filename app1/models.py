from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=200)
    author = models.TextField(max_length=20)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.TextField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Activity(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    name = models.TextField(max_length=20)
    team_size = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    activity_logo = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    activity = models.ManyToManyField(Activity,null=True)
    name = models.TextField(max_length=20)
    current_size = models.IntegerField(default = 0)
    team_lead = models.TextField(max_length=20,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    team_logo = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    team = models.ManyToManyField(Team)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    # activity = models.ManyToManyField(Activity)

    def __str__(self):
        return self.user.first_name

# class Logo(models.Model):
#     title = models.CharField(
#         max_length=80, blank=False, null=False)
#     #image_url = S3DirectField(dest='mediafiles/', blank=True)
#     picture = models.FileField(upload_to='media/', blank=True, null=False)