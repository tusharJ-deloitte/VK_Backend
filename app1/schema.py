import graphene
from .models import Category, Activity, Team, Player
from app1.types import CategoryType, ActivityType, TeamType, PlayerType
<<<<<<< HEAD
from .mutations import CreateCategory, UpdateCategory,DeleteCategory,CreateActivity,UpdateActivity,DeleteActivity
=======
from .mutations import CreateCategory, UpdateCategory, DeleteActivity, DeleteCategory, CreateActivity, UpdateActivity, CreateTeam, UpdateTeam

>>>>>>> Balaji

class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    all_categories = graphene.List(CategoryType)
    activity = graphene.Field(ActivityType,id=graphene.ID(required=True))
    all_activities = graphene.List(ActivityType)
    team = graphene.Field(TeamType,id=graphene.ID(required=True))
    all_teams = graphene.List(TeamType)
    player = graphene.Field(PlayerType,id=graphene.ID(required=True))
    all_players = graphene.List(PlayerType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_category(self, info, id):
        return Category.objects.get(id = id)

    def resolve_activity(self,info,id):
        return Activity.objects.get(id=id)

    def resolve_all_activities(self,info,**kwargs):
        return Activity.objects.all()

    def resolve_team(self,info,id):
        return Team.objects.get(id=id)

    def resolve_all_teams(self,info,**kwargs):
        return Team.objects.all()
    
    def resolve_player(self,info,id):
        return Player.objects.get(id=id)
    
    def resolve_all_players(self,info,**kwargs):
        return Player.objects.all()
        

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_activity = CreateActivity.Field()
    update_activity = UpdateActivity.Field()
    delete_activity = DeleteActivity.Field()
<<<<<<< HEAD
=======
    create_team = CreateTeam.Field()
    update_team = UpdateTeam.Field()
>>>>>>> Balaji

schema = graphene.Schema(query=Query, mutation=Mutation) 

