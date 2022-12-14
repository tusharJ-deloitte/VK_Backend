import app1.schema
import graphene
from app1.schema import Mutation

class Query(app1.schema.Query, graphene.ObjectType):
    pass

class Mutation(app1.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

