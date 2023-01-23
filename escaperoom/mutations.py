import graphene
from .types import DetailType, QuestionType, TallyType
from .models import Detail, Question, Tally
from app1.models import Event, Team


class CreateDetail(graphene.Mutation):
    class Arguments:
        theme = graphene.String()
        event_id = graphene.Int()
        bg_image = graphene.String()
        time = graphene.Int()
        number_of_questions = graphene.Int()
        level = graphene.Int()

    escapeRoomDetails = graphene.Field(DetailType)

    def mutate(self, info, theme, event_id, time, bg_image, number_of_questions, level):
        room_details_instance = Detail(
            theme=theme,
            event = Event.objects.get(id = event_id),
            time = time,
            bg_image=bg_image,
            number_of_questions=number_of_questions,
            level=level
        )
        room_details_instance.save()
        return CreateDetail(escapeRoomDetails=room_details_instance)


class DeleteDetail(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    escapeRoomDetails = graphene.Field(DetailType)

    def mutate(self, info, id):
        room_details_instance = Detail.objects.get(id=id)
        room_details_instance.delete()
        return DeleteDetail(escapeRoomDetails=room_details_instance)


class UpdateDetail(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        event_id = graphene.Int()
        time = graphene.Int()
        theme = graphene.String()
        bg_image = graphene.String()
        number_of_questions = graphene.Int()
        level = graphene.Int()

    escapeRoomDetails = graphene.Field(DetailType)

    def mutate(self, info, id, event_id, time ,theme, bg_image, number_of_questions, level):
        room_details_instance = Detail.objects.get(id=id)
        room_details_instance.event = Event.objects.get(id = event_id)
        room_details_instance.time = time
        room_details_instance.theme = theme
        room_details_instance.bg_image = bg_image
        room_details_instance.number_of_questions = number_of_questions
        room_details_instance.level = level
        room_details_instance.save()
        return UpdateDetail(escapeRoomDetails=room_details_instance)


class CreateQuestion(graphene.Mutation):
    class Arguments:
        escape_room_theme = graphene.String(required=True)
        context = graphene.String(required=True)
        number_of_images = graphene.Int(required=True)
        images = graphene.String(required=True)
        options = graphene.String()
        question_type = graphene.Int(required=True)
        question = graphene.String(required=True)
        answers = graphene.String(required=True)
        hints = graphene.String(required=True)

    question = graphene.Field(QuestionType)

    def mutate(self, info, escape_room_theme, images, options, context, number_of_images, question_type, question, answers, hints):
        question_instance = Question(
            escape_room=Detail.objects.get(theme=escape_room_theme),
            images=images,
            options=options,
            context=context,
            number_of_images=number_of_images,
            question_type=question_type,
            question=question,
            answers=answers,
            hints=hints
        )
        question_instance.save()
        return CreateQuestion(question=question_instance)


class UpdateQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        escape_room_theme = graphene.String(required=True)
        context = graphene.String(required=True)
        number_of_images = graphene.Int(required=True)
        images = graphene.String(required=True)
        options = graphene.String()
        question_type = graphene.Int(required=True)
        question = graphene.String(required=True)
        answers = graphene.String(required=True)
        hints = graphene.String(required=True)

    question = graphene.Field(QuestionType)

    # **update_data):
    def mutate(self, info, id, escape_room_theme, images, options, context, number_of_images, question_type, question, answers, hints):
        # question = Question.objects.filter(id=id)
        # if question:
        #     params = update_data
        #     print(params)
        #     question.update(**{k: v for k, v in params.items() if params[k]})
        #     print("updated")
        #     return UpdateQuestion(question=question.first())
        # else:
        #     print("!!!")
        # # escape_room_theme, images, options, context, number_of_images, question_type, question, answers, hints):
        question_instance = Question.objects.get(id=id)
        question_instance.escape_room = Detail.objects.get(
            theme=escape_room_theme)
        question_instance.context = context
        question_instance.number_of_images = number_of_images
        question_instance.images = images
        question_instance.options = options
        question_instance.question_type = question_type
        question_instance.question = question
        question_instance.answers = answers
        question_instance.hints = hints
        question_instance.save()
        return UpdateQuestion(question=question_instance)

class CreateTally(graphene.Mutation):
    class Arguments:
        event_id = graphene.Int()
        team_id = graphene.Int()
        final_score = graphene.Int()
        time_taken = graphene.Int()

    tallyDetails = graphene.Field(TallyType)

    def mutate(self, info,  team_id,event_id, final_score, time_taken):
        print("inside mutate")
        tally_instance = Tally(
            event = Event.objects.get(id = event_id),
            team = Team.objects.get(id = team_id),
            final_score = final_score,
            time_taken = time_taken
        )
        print("created")
        tally_instance.save()
        # tally_instance.event = Event.objects.get(id = event_id)
        # print(tally_instance.event)
        # tally_instance.save()
        return CreateTally(tallyDetails=tally_instance)
