from graphene_django.types import DjangoObjectType
from enum import IntEnum
# from django.contrib.auth.models import User
from .models import Detail, Question, Tally





class DetailType(DjangoObjectType):
    class Meta:
        model = Detail
        fields = ('id', 'theme', 'event','time','bg_image', 'number_of_questions', 'level')


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id','escape_room', 'images','options','context', 'number_of_images', 'question_type', 'question', 'answers', 'hints')

class TallyType(DjangoObjectType):
    class Meta:
        model = Tally
        fields = ('id','event', 'team','final_score','time_taken')

