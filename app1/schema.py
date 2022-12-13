import graphene
from .models import Category, Activity, Team, Player
from app1.types import CategoryType, ActivityType, TeamType, PlayerType
from .mutations import CreateCategory, UpdateCategory, DeleteActivity, DeleteCategory, CreateActivity, UpdateActivity, CreateTeam, UpdateTeam


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_category(self, info, id):
        return Category.objects.get(id = id)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_activity = CreateActivity.Field()
    update_activity = UpdateActivity.Field()
    delete_activity = DeleteActivity.Field()
    create_team = CreateTeam.Field()
    update_team = UpdateTeam.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 

