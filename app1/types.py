from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Category, Activity, Team, Player, Event, Registration


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # fields = ('id','name')
    exclude = ('password')


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_on')


class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'team_size', 'created_on',
                  'category_id', 'activity_logo')


class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        fields = ('id', 'name', 'created_on', 'activity_id',
                  'current_size', 'team_logo', 'team_lead', 'team_score')


class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = ('id', 'score', 'team_id', 'activity_id', 'user_id')


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ('id', 'name', 'activity', 'created_on' 'activity_mode', 'start_date', 'end_date', 'start_time', 'end_time',
                  'max_teams', 'max_members', 'first_prize', 'second_prize', 'third_prize', 'cur_participation', 'status')


class RegistrationType(DjangoObjectType):
    class Meta:
        model = Registration
        fields = ('id', 'event', 'team')
