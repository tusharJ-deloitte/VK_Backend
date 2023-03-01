from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Detail, Category, Activity, Team, Player, Event, Registration, IndRegistration, Pod, Upload,Quiz,QuizQuestion,Option,UserAnswer


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # fields = ('id','name')
    exclude = ('password')


class DetailType(DjangoObjectType):
    class Meta:
        model = Detail
        fields = ('id', 'user', 'employee_id',
                  'designation', 'profile_pic', 'doj')


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_on')


class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'team_size', 'created_on',
                  'category_id', 'activity_logo')


class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        fields = ('id', 'name', 'created_on', 'activity_id',
                  'current_size', 'team_logo', 'team_lead', 'team_score')


class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = ('id', 'score', 'team_id', 'activity_id', 'user_id')


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ('id', 'name', 'activity', 'created_on', 'event_type', 'activity_mode', 'start_date', 'end_date', 'start_time', 'end_time',
                  'min_members', 'max_members', 'cur_participation', 'status')


class RegistrationType(DjangoObjectType):
    class Meta:
        model = Registration
        fields = ('id', 'event', 'team')


class IndRegistrationType(DjangoObjectType):
    class Meta:
        model = IndRegistration
        fields = ('id', 'event', 'player')


class UploadType(DjangoObjectType):
    class Meta:
        model = Upload
        fields = ('id', 'user', 'event', 'is_uploaded', 'uploaded_on',
                  'file_name', 'file_size', 'file_duration', 'score')


class PodType(DjangoObjectType):
    class Meta:
        model = Pod
        fields = ('pod_id', 'user', 'pod_name', 'pod_size')

class QuizType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields=('id','event','banner_image','title','desc','last_modified')

class QuizQuestionType(DjangoObjectType):
    class Meta:
        model = QuizQuestion
        fields = ('id','quiz','question_text','image_clue','note','question_type','max_timer','points')

class OptionType(DjangoObjectType):
    class Meta:
        model = Option
        fields = ('id','question','option_text','is_correct')


class UserAnswerType(DjangoObjectType):
    class Meta:
        model = UserAnswer
        fields = ('id','user','quiz','question','submitted_answer','is_correct_answer','time_taken','score')

