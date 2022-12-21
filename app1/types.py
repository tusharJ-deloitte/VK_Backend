from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Category, Activity, Team, Player

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
        fields = ('id', 'name', 'team_size', 'created_on', 'category_id')

class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        fields = ('id', 'name', 'created_on','activity_id','current_size','team_logo','team_lead')

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = ('id', 'score', 'team_id','activity_id','user_id')