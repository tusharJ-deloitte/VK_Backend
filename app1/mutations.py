import graphene
from app1.types import CategoryType, TeamType, ActivityType, PlayerType
from .models import Category, Activity, Team, Player
import datetime

class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category_instance = Category(
            name = name
        )
        category_instance.save()
        return CreateCategory(category = category_instance)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name, ):
        category_instance = Category.objects.get(id = id)

        category_instance.name = name
        category_instance.created_on = datetime.datetime.utcnow

        print("-------------", category_instance.created_on)

        category_instance.save()

        return UpdateCategory(category = category_instance)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
    
    category = graphene.Field(CategoryType)
    def mutate(self,info,id):
        category_instance = Category.objects.get(id = id)
        category_instance.delete()
        return DeleteCategory(category = category_instance)

class CreateActivity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category = graphene.Int(required=True)
        # category = graphene.Field(CategoryType,required=True)
        team_size = graphene.Int(required=True)
    
    activity = graphene.Field(ActivityType)

    def mutate(self, info, name, category, team_size):
        activity_instance = Activity(
            name = name,
            category = Category.objects.get(id=category),
            team_size = team_size            
        )
        activity_instance.save()
        return CreateActivity(activity = activity_instance)

class UpdateActivity(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True)
        name=graphene.String()
        category_id = graphene.String()
        # team_size = graphene.Int()

    activity = graphene.Field(ActivityType)    

    def mutate(self, info, id, name,category_id):
        activity_instance = Activity.objects.get(id= id)
        activity_instance.name = name
        activity_instance.category = Category.objects.filter(name=category_id)[0]
        print(Category.objects.filter(name=category_id)[0])
        # activity_instance.team_size = team_size
        activity_instance.created_on = datetime.datetime.utcnow()
        activity_instance.save()

        print("----------------------------------------",activity_instance.category)
        
        return UpdateActivity(activity=activity_instance)

class DeleteActivity(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True)

    activity = graphene.Field(ActivityType)
    def mutate(self,info,id):
        activity_instance = Activity.objects.get(id=id)
        activity_instance.delete()
        return DeleteActivity(activity_instance)

class CreateTeam(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    team = graphene.Field(TeamType)
    def mutate(self, info, name, id):
        team_instance = Team(
            name=name,
            id = graphene.ID()
        )
        team_instance.save()
        return CreateTeam(team=team_instance)


class UpdateTeam(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    team = graphene.Field(TeamType)

    def mutate(self, info, id, name, ):
        team_instance = Team.objects.get(id=id)

        team_instance.name = name
        team_instance.created_on = datetime.datetime.utcnow

        print("-------------", team_instance.created_on)

        team_instance.save()

        return UpdateTeam(team=team_instance)
