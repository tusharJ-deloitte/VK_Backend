import escaperoom.schema
import graphene

class Query(escaperoom.schema.Query, graphene.ObjectType):
    pass

class Mutation(escaperoom.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


