import graphene
from app1.types import CategoryType
from .models import Category
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
        category_instance.created_on = datetime.datetime.utcnow(a2)

        print("-------------", category_instance.created_on)

        category_instance.save()

        return UpdateCategory(category = category_instance)


