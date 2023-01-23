from django.db import models
# from .types import LevelTypes
# from enum import IntEnum
# from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField
# from .models import Event
# from django.apps import apps

from app1.models import Event, Team

from .utils import LevelTypes, QuestionChoices

# Create your models here.

# app1 = apps.get_model("app1","Event")
class Detail(models.Model):

    # questions = models.ForeignKey(EscapeRoomQuestions, on_delete = models.CASCADE)
    theme = models.TextField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    bg_image = models.TextField()
    number_of_questions = models.IntegerField()
    time = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(
        choices=LevelTypes.choices(), default=LevelTypes.EASY)

    def __str__(self):
        return self.theme


class Question(models.Model):
    escape_room = models.ForeignKey(Detail, on_delete=models.CASCADE)
    context = models.TextField(null=True, blank=True)
    number_of_images = models.IntegerField(null=True, blank=True)
    images = models.JSONField(null=True, blank=True)
    question_type = models.IntegerField(
    choices=QuestionChoices.choices(), default=QuestionChoices.TEXTBOX, null=True, blank=True)
    question = models.TextField()
    options = models.JSONField(null=True, blank=True)
    answers = models.TextField(null=True, blank=True)
    hints = models.TextField(null=True)

    def __str__(self):
        return self.question


class Tally(models.Model):
    event= models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    final_score = models.IntegerField()
    time_taken = models.IntegerField()
    
