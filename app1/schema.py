import graphene
from .models import Category, Activity, Team, Player
from app1.types import CategoryType, ActivityType, TeamType, PlayerType

class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, name=graphene.String(required=True))
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_category(self, info, category_id):
        return Category.objects.get(id = category_id)

class Mutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name):
        category = Category.objects.get(pk = id)
        category.name = name
        category.save()

        return Mutation(category = category)

schema = graphene.Schema(query=Query, mutation=Mutation) 

