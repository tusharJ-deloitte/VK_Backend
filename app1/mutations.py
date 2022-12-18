import graphene
from app1.types import CategoryType,ActivityType
from .models import Category,Activity
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
        
 