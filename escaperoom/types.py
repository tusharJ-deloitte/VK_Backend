from graphene_django.types import DjangoObjectType
from enum import IntEnum
# from django.contrib.auth.models import User
from .models import Detail, Question





class DetailType(DjangoObjectType):
    class Meta:
        model = Detail
        fields = ('id', 'theme', 'bg_image', 'number_of_questions', 'level')


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id','escape_room_id', 'images','options','context', 'number_of_images', 'question_type', 'question', 'answers', 'hints')



