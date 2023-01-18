import graphene
from .models import Detail, Question
from .types import DetailType, QuestionType
from .mutations import CreateDetail, DeleteDetail


class Query(graphene.ObjectType):
    detail = graphene.Field(DetailType, id=graphene.ID(required=True))
    all_details = graphene.List(DetailType)


    def resolve_all_details(self, info, **kwargs):
        return Detail.objects.all()

    def resolve_detail(self, info, id):
        return Detail.objects.get(id=id)



class Mutation(graphene.ObjectType):

    #escaperoom mutations
    create_detail = CreateDetail.Field()
    delete_detail = DeleteDetail.Field()


    



schema = graphene.Schema(query=Query, mutation=Mutation)
