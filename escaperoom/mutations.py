import graphene
from .types import DetailType, QuestionType
from .models import Detail, Question


class CreateDetail(graphene.Mutation):
    class Arguments:
        theme = graphene.String()
        bg_image = graphene.String()
        number_of_questions = graphene.Int()
        level = graphene.Int()

    escapeRoomDetails = graphene.Field(DetailType)

    def mutate(self, info, theme,bg_image, number_of_questions, level):
        room_details_instance = Detail(
            theme= theme, 
            bg_image = bg_image, 
            number_of_questions = number_of_questions,
            level = level
            )
        room_details_instance.save()
        return CreateDetail(escapeRoomDetails = room_details_instance)


