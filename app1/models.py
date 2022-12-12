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
    created_on = models.DateTimeField()

    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    activity = models.ManyToManyField(Activity)
    name = models.TextField(max_length=20)
    created_on = models.DateTimeField()

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name