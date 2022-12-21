import graphene
from app1.types import CategoryType,ActivityType,TeamType,PlayerType
from .models import Category,Activity,Team,Player
import datetime
from django.contrib.auth.models import User

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
        print("-------------------------------------------------------")

    category = graphene.Field(CategoryType)    

    def mutate(self, info, id, name ):
        category_instance = Category.objects.get(id= id)
        
        category_instance.name = name
        category_instance.created_on = datetime.datetime.utcnow()

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
        category_id = graphene.Int()
        team_size = graphene.Int()

    activity = graphene.Field(ActivityType)    

    def mutate(self, info, id, name,category_id,team_size):
        print("inside mutate")
        activity_instance = Activity.objects.get(id= id)
        activity_instance.name = name
        activity_instance.category = Category.objects.get(id=category_id)#filter(name=category_id)[0]
        # print(Category.objects.filter(name=category_id)[0])
        
        activity_instance.team_size = team_size
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
        activity = graphene.String()
        currentSize = graphene.Int()
        teamLead = graphene.String()

        # print(name,activity)
    team = graphene.Field(TeamType)
    print("!!!!!!!!!!!!",team)
    def mutate(self, info, name,currentSize,teamLead,activity):
        print("inside mutate")
        # print(Activity.objects.filter(name=activity))
        team_instance = Team(
            name=name,
            current_size = currentSize,
            team_lead = teamLead

            )

        # print("0")
            # id = graphene.ID(),
            # activity = Activity.objects.get(id=activity)[0]
        team_instance.save()
        activity = Activity.objects.filter(name=activity)[0]
        team_instance.activity.add(activity)
        team_instance.save()
        # print("1")
        print("--------------------",team_instance)

        
        # print("--------------------",team_instance)
        # team_instance.activity = Activity.objects.get(id=activity)[0]
        # print("==========",Activity.objects.get(id=activity))
        # print("--------------------",team_instance.activity)

        
        return CreateTeam(team=team_instance)


# class UpdateTeam(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#         name = graphene.String()

#     team = graphene.Field(TeamType)

#     def mutate(self, info, id, name, ):
#         team_instance = Team.objects.get(id=id)

#         team_instance.name = name
#         team_instance.created_on = datetime.datetime.utcnow()
#         team_instance.save()
#         return UpdateTeam(teamactivity = Activity.objects.get(id=activity)
#         # team_instance.activity.add(activity)
#         # team_instance.save()=team_instance)

class CreatePlayer(graphene.Mutation):
    class Arguments:
        team_name = graphene.String(required=True)
        username = graphene.String(required=True)
        score = graphene.Int()
        activity = graphene.String()
        
    player = graphene.Field(PlayerType)
    def mutate(self,info,team_name,username,score,activity):
        print("inside")
        player_instance = Player(
            
            user = User.objects.get(username=username),
            score = score 
        )
        player_instance.save()
        activity_instance = Activity.objects.filter(name=activity)[0]
        print(activity_instance)
        player_instance.activity.add(activity_instance)
        player_instance.save()
        print("000")
        team_instance = Team.objects.filter(name=team_name)[0]
        print(team_instance)
        player_instance.team.add(team_instance)
        print(team_instance)
        
        return CreatePlayer(player_instance)

class UpdatePlayer(graphene.Mutation):
    class Arguments:
        player_id = graphene.Int(required=True)
        team_id = graphene.Int()
        username = graphene.String()
        score = graphene.Int()

    player = graphene.Field(PlayerType)
    def mutate(self,info,player_id,team_id=0,username="",score=0):
        player_instance = Player.objects.get(id=player_id)
        if team_id != 0:
            player_instance.team = Team.objects.get(id = team_id)
        if username != "":
            player_instance.user = User.objects.get(username=username)
        if score!=0:
            player_instance.score = score
        player_instance.save()
        return UpdatePlayer(player_instance)

class DeletePlayer(graphene.Mutation):
    class Arguments:
        player_id = graphene.Int(required=True)

    player = graphene.Field(PlayerType)
    def mutate(self,info,player_id):
        player_instance = Player.objects.get(id=player_id)
        player_instance.delete()
        return DeletePlayer(player_instance)
        