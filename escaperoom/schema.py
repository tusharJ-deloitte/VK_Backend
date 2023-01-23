import graphene
from .models import Detail, Question, Tally
from .types import DetailType, QuestionType, TallyType
from .mutations import CreateDetail, DeleteDetail, UpdateDetail, CreateQuestion, UpdateQuestion, CreateTally


class Query(graphene.ObjectType):
    detail = graphene.Field(DetailType, id=graphene.ID(required=True))
    all_details = graphene.List(DetailType)
    question = graphene.Field(QuestionType, id=graphene.ID(required=True))
    all_questions = graphene.List(QuestionType)
    tally = graphene.Field(TallyType, id=graphene.ID(required=True))
    all_tallys = graphene.List(TallyType)

    def resolve_all_tallys(self, info, **kwargs):
        return Tally.objects.all()

    def resolve_tally(self, info, id):
        return Tally.objects.get(id=id)

    def resolve_all_details(self, info, **kwargs):
        return Detail.objects.all()

    def resolve_detail(self, info, id):
        return Detail.objects.get(id=id)

    def resolve_all_questions(self, info, **kwargs):
        return Question.objects.all()

    def resolve_question(self, info, id):
        return Question.objects.get(id=id)


class Mutation(graphene.ObjectType):

    # escaperoom mutations
    create_detail = CreateDetail.Field()
    delete_detail = DeleteDetail.Field()
    update_detail = UpdateDetail.Field()
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    create_tally = CreateTally.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
