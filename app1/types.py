from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from app1.models import Category, Activity, Team, Player

class UserType(DjangoObjectType):
    class Meta:
        model = User
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
        fields = ('id', 'name', 'created_on')

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = ('id', 'score', 'team_id', 'user_id')