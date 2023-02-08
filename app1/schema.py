import graphene
from .models import Detail, Category, Activity, Team, Player, Event, Registration, Upload, Pod
from app1.types import DetailType, UserType, CategoryType, ActivityType, TeamType, PlayerType, EventType, RegistrationType, UploadType,PodType
from .mutations import CreateUser, CreateCategory, UpdateCategory, DeleteCategory, CreateActivity, UpdateActivity, DeleteActivity, CreateTeam, CreatePlayer, UpdatePlayer, DeletePlayer, CreateEvent, CreateRegistration, UpdateTeamScores, CreateUpload,CreatePod
from django.contrib.auth.models import User

class Query(graphene.ObjectType):

    detail = graphene.Field(DetailType,id=graphene.ID(required=True))
    all_details = graphene.List(DetailType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    all_users = graphene.List(UserType)
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    all_categories = graphene.List(CategoryType)
    activity = graphene.Field(ActivityType, id=graphene.ID(required=True))
    all_activities = graphene.List(ActivityType)
    team = graphene.Field(TeamType, id=graphene.ID(required=True))
    all_teams = graphene.List(TeamType)
    player = graphene.Field(PlayerType,
                            id=graphene.ID(required=True))
    all_players = graphene.List(PlayerType)

    event = graphene.Field(EventType,
                           id=graphene.ID(required=True))
    all_events = graphene.List(EventType)

    registration = graphene.Field(RegistrationType,
                                  id=graphene.ID(required=True))
    all_registrations = graphene.List(RegistrationType)

    upload = graphene.Field(UploadType, id=graphene.ID(required=True))
    all_uploads = graphene.List(UploadType)
    pod = graphene.Field(PodType,id=graphene.ID(required=True))
    all_pods = graphene.List(PodType)

    def resolve_all_detais(self,info,**kwargs):
        return Detail.objects.all()

    def resolve_detail(self, info, id):
        return Detail.objects.get(id=id)
    
    def resolve_all_users(self,info,**kwargs):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, id):
        return Category.objects.get(id=id)

    def resolve_activity(self, info, id):
        return Activity.objects.get(id=id)

    def resolve_all_activities(self, info, **kwargs):
        return Activity.objects.all()

    def resolve_team(self, info, id):
        return Team.objects.get(id=id)

    def resolve_all_teams(self, info, **kwargs):
        return Team.objects.all()

    def resolve_player(self, info, id):
        return Player.objects.get(id=id)

    def resolve_all_players(self, info, **kwargs):
        return Player.objects.all()

    def resolve_event(self, info, id):
        return Event.objects.get(id=id)

    def resolve_all_events(self, info, **kwargs):
        return Event.objects.all()

    def resolve_registration(self, info, id):
        return Registration.objects.get(id=id)

    def resolve_all_registrations(self, info, **kwargs):
        return Registration.objects.all()

    def resolve_upload(self, info, id):
        return Upload.objects.get(id=id)

    def resolve_all_uploads(self, info, **kwargs):
        return Upload.objects.all()

    def resolve_pod(self, info, id):
        return Pod.objects.get(id=id)

    def resolve_all_pods(self, info, **kwargs):
        return Pod.objects.all()
    


class Mutation(graphene.ObjectType):
    #category mutations
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

    #activity mutations
    create_activity = CreateActivity.Field()
    update_activity = UpdateActivity.Field()
    delete_activity = DeleteActivity.Field()

    #team mutations
    create_team = CreateTeam.Field()
    # update_team = UpdateTeam.Field()

    #player mutations
    create_player = CreatePlayer.Field()
    update_player = UpdatePlayer.Field()
    delete_player = DeletePlayer.Field()

    #event mutations
    create_event = CreateEvent.Field()

    #registrations mutations
    create_registration = CreateRegistration.Field()

    #update team score
    update_team_scores = UpdateTeamScores().Field()

    #plank(upload) mutations
    create_upload = CreateUpload.Field()

    create_user = CreateUser.Field()

    create_pod = CreatePod.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
