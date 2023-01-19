from django.db import models
# from .types import LevelTypes
# from enum import IntEnum
# from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

from .utils import LevelTypes, QuestionChoices

# Create your models here.


class Detail(models.Model):

    # questions = models.ForeignKey(EscapeRoomQuestions, on_delete = models.CASCADE)
    theme = models.TextField(max_length = 20)
    bg_image = models.TextField()
    number_of_questions = models.IntegerField()
    time = models.TimeField(null = True, blank = True)
    level = models.IntegerField(choices= LevelTypes.choices(), default=LevelTypes.EASY)

    def __str__(self):
        return self.theme

class Question(models.Model):
    escape_room = models.ForeignKey(Detail, on_delete = models.CASCADE)
    context = models.TextField()
    number_of_images = models.IntegerField()
    images = models.JSONField(null =True, blank = True)
    question_type = models.IntegerField(choices= QuestionChoices.choices(), default=QuestionChoices.TEXTBOX)
    question = models.TextField()
    options = models.JSONField(null = True, blank = True)
    answers = models.TextField()
    hints = models.TextField(null = True)
