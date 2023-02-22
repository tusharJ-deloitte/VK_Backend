import graphene
from app1.types import UserType, CategoryType, ActivityType, TeamType, PlayerType, EventType, RegistrationType, IndRegistrationType, PodType, UploadType
from .models import Detail, User, Category, Activity, Team, Player, Event, Registration, IndRegistration, Pod, Upload
import datetime
from django.contrib.auth.models import User
from graphql import GraphQLError


class CreateUser(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int()
        name = graphene.String()
        email = graphene.String()
        designation = graphene.String()
        doj = graphene.Date()
        profile_pic = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, name, email, designation, doj, employee_id, profile_pic):
        print("inside createUser mutation")
        if " " in name:
            fname = name.split(' ', 1)[0]
            lname = name.split(' ', 1)[1]
        else:
            fname = name
            lname = ""
        user_instance = User(
            email=email,
            username=email.split('@')[0],
            first_name=fname,
            last_name=lname
        )
        print(user_instance)
        user_instance.save()
        detail_instance = Detail(
            user=user_instance,
            employee_id=employee_id,
            designation=designation,
            doj=doj,
            profile_pic=profile_pic
        )
        detail_instance.save()
        print("outside createUser mutation")
        return CreateUser(user=user_instance)


class CreateUser(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int()
        name = graphene.String()
        email = graphene.String()
        designation = graphene.String()
        doj = graphene.Date()
        profile_pic = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, name, email, designation, doj, employee_id, profile_pic):
        print("inside createUser mutation")
        if " " in name:
            fname = name.split(' ', 1)[0]
            lname = name.split(' ', 1)[1]
        else:
            fname = name
            lname = ""
        user_instance = User(
            email=email,
            username=email.split('@')[0],
            first_name=fname,
            last_name=lname
        )
        print(user_instance)
        user_instance.save()
        detail_instance = Detail(
            user=user_instance,
            employee_id=employee_id,
            designation=designation,
            doj=doj,
            profile_pic=profile_pic
        )
        detail_instance.save()
        print("outside createUser mutation")
        return CreateUser(user=user_instance)


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category_instance = Category(
            name=name
        )
        category_instance.save()
        print(category_instance)
        return CreateCategory(category=category_instance)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        print("-------------------------------------------------------")

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name):
        category_instance = Category.objects.get(id=id)

        category_instance.name = name
        category_instance.created_on = datetime.datetime.utcnow()

        category_instance.save()

        return UpdateCategory(category=category_instance)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, id):
        category_instance = Category.objects.get(id=id)
        category_instance.delete()
        return DeleteCategory(category=category_instance)


class CreateActivity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category = graphene.Int(required=True)
        # category = graphene.Field(CategoryType,required=True)
        team_size = graphene.Int(required=True)

    activity = graphene.Field(ActivityType)

    def mutate(self, info, name, category, team_size):
        activity_instance = Activity(
            name=name,
            category=Category.objects.get(id=category),
            team_size=team_size
        )
        activity_instance.save()
        return CreateActivity(activity=activity_instance)


class UpdateActivity(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        category_id = graphene.Int()
        team_size = graphene.Int()

    activity = graphene.Field(ActivityType)

    def mutate(self, info, id, name, category_id, team_size):
        print("inside mutate")
        activity_instance = Activity.objects.get(id=id)
        activity_instance.name = name
        activity_instance.category = Category.objects.get(
            id=category_id)  # filter(name=category_id)[0]
        # print(Category.objects.filter(name=category_id)[0])

        activity_instance.team_size = team_size
        activity_instance.created_on = datetime.datetime.utcnow()
        activity_instance.save()

        print("----------------------------------------",
              activity_instance.category)

        return UpdateActivity(activity=activity_instance)


class DeleteActivity(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    activity = graphene.Field(ActivityType)

    def mutate(self, info, id):
        activity_instance = Activity.objects.get(id=id)
        activity_instance.delete()
        return DeleteActivity(activity_instance)


class CreateTeam(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        activity = graphene.String()
        currentSize = graphene.Int()
        teamLead = graphene.String()
        team_logo = graphene.String()

        # print(name,activity)
    team = graphene.Field(TeamType)
    print("!!!!!!!!!!!!", team)

    def mutate(self, info, name, currentSize, teamLead, activity, team_logo):
        print("inside mutate")
        # print(Activity.objects.filter(name=activity))
        team_instance = Team(
            name=name,
            current_size=currentSize,
            team_lead=teamLead,
            team_logo=team_logo
        )

        # print("0")
        # id = graphene.ID(),
        # activity = Activity.objects.get(id=activity)[0]
        team_instance.save()
        activity = Activity.objects.filter(name=activity)[0]
        team_instance.activity.add(activity)
        team_instance.save()
        # print("1")
        print("--------------------", team_instance)

        # print("--------------------",team_instance)
        # team_instance.activity = Activity.objects.get(id=activity)[0]
        # print("==========",Activity.objects.get(id=activity))
        # print("--------------------",team_instance.activity)

        return CreateTeam(team=team_instance)


# class UpdateTeam(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#         name = graphene.String()
#         activity = graphene.Int()


#     team = graphene.Field(TeamType)

#     def mutate(self, info, id, name, activity ):
#         team_instance = Team.objects.get(id=id)

#         team_instance.name = name
#         team_instance.activity = Activity.objects.get(id = activity)
#         team_instance.created_on = datetime.datetime.utcnow()
#         team_instance.save()
#         return UpdateTeam(team = team_instance)
#         # team_instance.activity.add(activity)
#         # team_instance.save()=team_instance)

class CreatePlayer(graphene.Mutation):
    class Arguments:
        team_name = graphene.String()
        user_email = graphene.String(required=True)
        score = graphene.Int()
        activity_id = graphene.Int()

    player = graphene.Field(PlayerType)

    def mutate(self, info, team_name, user_email, score, activity_id):
        print("inside")
        player_instance = Player(

            user=User.objects.get(email=user_email),
            score=score,
            activity_id=activity_id
        )
        player_instance.save()
        # activity_instance = Activity.objects.filter(name=activity)[0]
        # print(activity_instance)
        # player_instance.activity.add(activity_instance)
        # player_instance.save()
        print("000")

        team_instance = Team.objects.filter(name=team_name)[0]
        print(team_instance)
        player_instance.team.add(team_instance)
        print(team_instance)

        return CreatePlayer(player_instance)


class CreateIndPlayer(graphene.Mutation):
    class Arguments:
        user_email = graphene.String(required=True)
        score = graphene.Int()
        activity_id = graphene.Int()

    player = graphene.Field(PlayerType)

    def mutate(self, info, user_email, score, activity_id):
        print("inside")
        player_instance = Player(

            user=User.objects.get(email=user_email),
            score=score,
            activity_id=activity_id
        )
        player_instance.save()

        return CreateIndPlayer(player_instance)


class CreateEvent(graphene.Mutation):
    class Arguments:
        activity_name = graphene.String(required=True)
        name = graphene.String(required=True)
        activity_mode = graphene.String(required=True)
        event_type = graphene.String()
        min_members = graphene.Int()
        max_members = graphene.Int()
        start_date = graphene.Date()
        end_date = graphene.Date()
        start_time = graphene.Time()
        end_time = graphene.Time()

    event = graphene.Field(EventType)

    def mutate(self, info, activity_name, name, activity_mode, min_members, max_members, start_date, end_date, start_time, end_time, event_type):
        print("inside")
        print(name)
        print(datetime.datetime.now().date())   
        event_instance = Event(
            activity=Activity.objects.get(name=activity_name),
            activity_mode=activity_mode,
            name=name,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            min_members=min_members,
            max_members=max_members,
            event_type=event_type

        )

        event_instance.save()
        print("outside")

        # activity_instance = Activity.objects.filter(name=activity)[0]
        # print(activity_instance)
        # player_instance.activity.add(activity_instance)
        # player_instance.save()

        return CreateEvent(event=event_instance)


class CreateIndEvent(graphene.Mutation):
    class Arguments:
        activity_name = graphene.String(required=True)
        name = graphene.String(required=True)
        activity_mode = graphene.String(required=True)
        event_type = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        start_time = graphene.Time()
        end_time = graphene.Time()

    event = graphene.Field(EventType)

    def mutate(self, info, activity_name, name, activity_mode, start_date, end_date, start_time, end_time, event_type):
        print("inside")
        print(datetime.datetime.now().date())
        event_instance = Event(
            activity=Activity.objects.get(name=activity_name),
            activity_mode=activity_mode,
            name=name,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            event_type=event_type

        )

        event_instance.save()
        print("outside")

        # activity_instance = Activity.objects.filter(name=activity)[0]
        # print(activity_instance)
        # player_instance.activity.add(activity_instance)
        # player_instance.save()

        return CreateIndEvent(event=event_instance)


class UpdatePlayer(graphene.Mutation):
    class Arguments:
        player_id = graphene.Int(required=True)
        team_id = graphene.Int()
        username = graphene.String()
        score = graphene.Int()

    player = graphene.Field(PlayerType)

    def mutate(self, info, player_id, team_id=0, username="", score=0):
        player_instance = Player.objects.get(id=player_id)
        if team_id != 0:
            player_instance.team = Team.objects.get(id=team_id)
        if username != "":
            player_instance.user = User.objects.get(username=username)
        if score != 0:
            player_instance.score = score
        player_instance.save()
        return UpdatePlayer(player_instance)


class DeletePlayer(graphene.Mutation):
    class Arguments:
        player_id = graphene.Int(required=True)

    player = graphene.Field(PlayerType)

    def mutate(self, info, player_id):
        player_instance = Player.objects.get(id=player_id)
        player_instance.delete()
        return DeletePlayer(player_instance)


class CreateRegistration(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID()
        team_id = graphene.ID()

    reg = graphene.Field(RegistrationType)

    def mutate(self, info, event_id, team_id):
        print("inside")
        reg_instance = Registration(
            team=Team.objects.get(id=team_id),
            event=Event.objects.get(id=event_id)
        )
        reg_instance.save()
        print("outside")

        return CreateRegistration(reg=reg_instance)


class CreateIndRegistration(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID()
        player_id = graphene.ID()

    reg = graphene.Field(IndRegistrationType)

    def mutate(self, info, event_id, player_id):
        print("inside")
        reg_instance = IndRegistration(
            player=Player.objects.get(id=player_id),
            event=Event.objects.get(id=event_id)
        )
        reg_instance.save()
        print("outside")

        return CreateIndRegistration(reg=reg_instance)

# update team scores and then players score as well


class UpdateTeamScores(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID()
        first_prize_team_id = graphene.ID()
        second_prize_team_id = graphene.ID()
        third_prize_team_id = graphene.ID()

    event = graphene.Field(EventType)

    def mutate(self, info, event_id, first_prize_team_id, second_prize_team_id, third_prize_team_id):
        print("inside mutate function of update event score")
        event_instance = Event.objects.get(id=event_id)

        prize_list = [first_prize_team_id,
                      second_prize_team_id, third_prize_team_id]

        prize_score = [event_instance.first_prize,
                       event_instance.second_prize, event_instance.third_prize]

        for i in range(3):
            team_instance = Team.objects.get(id=prize_list[i])
            team_instance.team_score = prize_score[i]
            all_players_of_team = Player.team.through.objects.filter(
                team_id=prize_list[i])
            for player in all_players_of_team:
                player_instance = Player.objects.get(id=player.player_id)
                # giving all players same score
                player_instance.score = prize_score[i]
                player_instance.save()
            team_instance.save()

        print("done")
        return UpdateTeamScores(event=event_instance)


class CreateUpload(graphene.Mutation):
    class Arguments:
        user_email = graphene.String(required=True)
        event_name = graphene.String(required=True)
        file_duration = graphene.String(required=True)
        file_size = graphene.Int(required=True)

    upload = graphene.Field(UploadType)

    def mutate(self, info, user_email, event_name, file_duration,file_size):
        upload_instance = Upload(
            user=User.objects.get(email=user_email),
            event=Event.objects.get(name=event_name),
            file_duration=file_duration,
            file_size=file_size
        )
        upload_instance.save()
        return CreateUpload(upload_instance)


class CreatePod(graphene.Mutation):
    class Arguments:
        pod_id = graphene.Int(required=True)
        user_email = graphene.String(required=True)
        name = graphene.String(required=True)
        size = graphene.Int(required=True)

    pod = graphene.Field(PodType)

    def mutate(self, info, pod_id, user_email, name, size):
        pod_instance = Pod(
            pod_id=pod_id,
            user=User.objects.get(email=user_email),
            pod_name=name,
            pod_size=size
        )
        pod_instance.save()
        return CreatePod(pod_instance)
