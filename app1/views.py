from django.shortcuts import render
from .models import Activity, Player, Team, Category, Event, Registration
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import io
from rest_framework.parsers import JSONParser
from .schema import schema
import json
from django.contrib.auth.models import User
from rest_framework import viewsets
import base64
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.db.models import Sum, Count
import datetime


def home(request):
    return render(request, 'app1/home.html')


def is_admin(request, userId):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=userId)
            adminUser = []
            if user.is_superuser:
                adminUser.append({"isAdmin": 1})
            else:
                adminUser.append({"isAdmin": 0})
            json_post = json.dumps(adminUser)
            return HttpResponse(json_post, content_type='application/json')
        except:
            return HttpResponse("Error Occured", content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_category(request, pk):
    if request.method == 'GET':
        result = schema.execute(
            '''
            query getCategory ($id : ID!){
                category (id : $id) {

                    name
                    createdOn
                }
            }
            ''', variables={'id': pk}
        )

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def create_category(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data["name"])

        result = schema.execute(
            '''
            mutation firstMutation ($name : String!){
	            createCategory(name : $name){
                    category {
                        id
                        name
                    }
                }
            }
            ''', variables={'name': python_data["name"]}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    else:
        return HttpResponse("wrong request", content_type='application/json')


def update_category(request, pk):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data["name"])

        result = schema.execute(
            '''
            mutation updateMutation ($id : ID!, $name : String!){
	            updateCategory(id : $id, name : $name){
                    category {
                        id
                        name
                        createdOn
                    }
                }
            }
            ''', variables={'id': pk, 'name': python_data["name"]}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    else:
        return HttpResponse("wrong request", content_type='application/json')


def delete_category(request, pk):
    if request.method == 'DELETE':
        result = schema.execute(
            '''
            mutation deleteCategory ($id : ID!){
                deleteCategory (id : $id) {
                    category {
                        name
                    }
                }
            }
            ''', variables={'id': pk}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    else:
        return HttpResponse("wrong request", content_type='application/json')


def create_activity(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data["name"])

        result = schema.execute(
            '''
            mutation createActivity($name : String!,$category: Int!,$teamSize:Int!){
               createActivity(name:$name,category:$category,teamSize:$teamSize){
                   activity{
                       name
                       id
                       teamSize
                   }
               }
           }
            ''', variables={'name': python_data["name"], 'category': python_data["category"], 'teamSize': python_data["teamSize"]}
        )

        print("------------------------")
        print("final result : ",  result)

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def update_activity(request, pk):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

        result = schema.execute(
            '''
            mutation updateActivity($id:ID!,$name : String!,$categoryId:Int!,$teamSize:Int!){
	            updateActivity(id:$id,name : $name,categoryId:$categoryId,teamSize:$teamSize){
                    activity{
                        id
                        name
                        createdOn
                        teamSize
                        category{
                            id
                            name
                        }
                    }
                }
            }
            ''', variables={'id': pk, 'name': python_data["name"], 'categoryId': python_data['categoryId'], 'teamSize': python_data['teamSize']}
        )

        print("------------------------")
        print("final result : ",  result)

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_activity(request, pk):
    if request.method == "GET":
        result = schema.execute(
            '''
            query getActivity ($id : ID!){
                activity(id : $id) {
                    id
                    name
                    createdOn
                    teamSize
                }
            }
            ''', variables={'id': pk}
        )

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_activity_list(request):
    if request.method == 'GET':
        response = [item.name for item in Activity.objects.all()]
        json_post = json.dumps(response)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def delete_activity(request, pk):
    if request.method == 'DELETE':
        result = schema.execute(
            '''
            mutation deleteActivity ($id : ID!){
                deleteActivity(id : $id) {
                    activity{
                        name
                    }
                }
            }
            ''', variables={'id': pk}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    else:
        return HttpResponse("wrong request", content_type='application/json')


def create_teams(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        result = schema.execute(
            '''
            mutation createTeams($name : String!,$activity: String!,$currentSize:Int!,$teamLead:String!,$teamLogo:String!){
               createTeam(name:$name,activity:$activity,teamLead:$teamLead,currentSize:$currentSize, teamLogo:$teamLogo){
                    team{
                        id
                    }
                }

            }


            ''', variables={'name': python_data["name"], 'activity': python_data["activity"], 'currentSize': python_data["currentSize"], 'teamLead': python_data["teamLead"], 'teamLogo': python_data["team_logo"]}
        )
        activity_id = Activity.objects.get(name=python_data["activity"]).pk
        print(activity_id)

        # team = Team.objects.get(name = python_data["name"])
        # team.team_logo = Te
        for item in range(0, python_data["currentSize"]):
            user_email = python_data['players'][item]
            result1 = schema.execute(
                '''
                        mutation createPlayer($teamName:String!,$userEmail:String!,$score:Int!,$activityId:Int!){
                            createPlayer(teamName:$teamName,userEmail:$userEmail,score:$score,activityId:$activityId){

                                player{
                                    id
                                    score
                                }
                            }
                        }

                        ''', variables={'teamName': python_data["name"], 'userEmail': user_email, 'score': 0, 'activityId': activity_id}
            )

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def update_teams(request, team_id):
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        team_instance = Team.objects.get(id=team_id)
        team_instance.name = python_data['name']
        team_instance.team_lead = python_data['teamLead']
        team_instance.current_size = python_data['currentSize']
        team_instance.team_logo = python_data["team_logo"]
        team_instance.save()

        activity_instance = Activity.objects.filter(
            name=python_data['activity'])[0]
        print(activity_instance)
        team_instance.activity.add(activity_instance)
        team_instance.save()

        players = Player.team.through.objects.filter(team_id=team_id)

        # print("------- : ", players)
        existing_players = []

        for player in players:
            existing_players.append(Player.objects.get(
                id=player.player_id).user.email)

        print("--------\n", existing_players)

        d = {}

        for player in existing_players:
            d[player] = -1

        for player in python_data["players"]:
            if player in d.keys():
                d[player] = d[player] + 1
            else:
                d[player] = 1

        print("********", d)

        for key, value in d.items():
            username = User.objects.get(email=key).first_name
            id = User.objects.get(email=key).pk
            print(username, id)

            if value == 1:
                result1 = schema.execute(
                    '''
                        mutation createPlayer($teamName:String!,$userEmail:String!,$score:Int!){
                            createPlayer(teamName:$teamName,userEmail:$userEmail,score:$score){

                                player{
                                    id
                                    score
                                }
                            }
                        }

                        ''', variables={'teamName': python_data["name"], 'userEmail': key, 'score': 0}
                )

            elif value == -1:
                l = []
                p_id = Player.objects.filter(user_id=id)
                for item in p_id:
                    l.append(item.pk)

                t_id = Player.team.through.objects.filter(team_id=team_id)
                for item in t_id:
                    if item.player_id in l:
                        Player.objects.get(id=item.player_id).delete()

        return HttpResponse({"msg": "successful"}, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def delete_teams(request, team_id):
    if request.method == 'DELETE':
        pt = Player.team.through.objects.filter(team_id=team_id)

        for item in pt:
            Player.objects.get(id=item.player_id).delete()

        Team.objects.get(id=team_id).delete()
        return HttpResponse(200)
    else:
        return HttpResponse("wrong request", content_type='application/json')


def manage_teams(request, user_id):
    if request.method == 'GET':

        players = Player.objects.filter(user_id=user_id)

        teams = []

        for player in players:
            teams.append(Player.team.through.objects.get(
                player_id=player.id).team_id)

        print("teams : ", teams)

        response = []

        for team in teams:
            team_id = team
            team_object = Team.objects.get(id=team_id)
            team_name = team_object.name
            team_lead = team_object.team_lead
            team_size = team_object.current_size

            team_lead = team_object.team_lead
            team_logo = team_object.team_logo
            team_mem_ids = Player.team.through.objects.filter(team_id=team_id)

            print("team_mem_ids", team_mem_ids)
            team_mem = []
            for id in team_mem_ids:
                user_id = Player.objects.get(id=id.player_id).user_id
                print("inside for id : ", user_id)
                user_object = User.objects.get(id=user_id)
                first_name = user_object.first_name
                last_name = user_object.last_name
                user_email = user_object.email
                p = {

                    "first_name": first_name,
                    "last_name": last_name,
                    "user_email": user_email
                }
                team_mem.append(p)

            activity_object = Team.activity.through.objects.filter(
                team_id=team_id)
            activity_name = Activity.objects.get(
                id=activity_object[0].activity_id).name
            activity_size = Activity.objects.get(
                id=activity_object[0].activity_id).team_size
            category_id = Activity.objects.get(
                id=activity_object[0].activity_id).category_id
            activity_logo = Activity.objects.get(
                id=activity_object[0].activity_id).activity_logo
            category_name = Category.objects.get(id=category_id).name
            temp_response = {
                "team_id": team_id,
                "team_name": team_name,
                "team_size": team_size,
                "team_lead": team_lead,
                "team_logo": team_logo,
                "team_mem": team_mem,
                "activity_name": activity_name,
                "actvity_size": activity_size,
                "activity_logo": activity_logo,
                "category_name": category_name

            }
            print("team_id", temp_response)
            response.append(temp_response)

        json_post = json.dumps(response)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def create_event(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        result = schema.execute(
            '''
            mutation createEvent($name : String!,$activityName: String!,$activityMode: String!,$maxTeams:Int!,$maxMembers:Int!,$firstPrize:Int!,$secondPrize:Int!,$thirdPrize:Int!,$startDate:Date!,$endDate:Date!,$startTime:Time!,$endTime:Time!){
               createEvent(name:$name,activityName:$activityName,activityMode:$activityMode,maxTeams:$maxTeams,maxMembers:$maxMembers, firstPrize:$firstPrize,secondPrize:$secondPrize,thirdPrize:$thirdPrize,startTime:$startTime,endTime:$endTime,startDate:$startDate,endDate:$endDate){
                    event{
                        name
                    }
                }

            }


            ''', variables={'name': python_data["name"], 'activityName': python_data["activityName"], 'activityMode': python_data['activityMode'], 'maxTeams': python_data["maxTeams"], 'maxMembers': python_data["maxMembers"], 'firstPrize': python_data["firstPrize"], 'secondPrize': python_data["secondPrize"], 'thirdPrize': python_data["thirdPrize"], 'startDate': python_data['startDate'], 'endDate': python_data['endDate'], 'startTime': python_data['startTime'], 'endTime': python_data['endTime']}
        )

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_all_events(request):
    if request.method == 'GET':
        result = schema.execute(
            '''query{
                    allEvents{
                        id,
                        createdOn,
                        name,
                        activityMode,
                        maxTeams,
                        maxMembers,
                        curParticipation,
                        startDate,
                        endDate,
                        startTime,
                        endTime,
                        firstPrize,
                        secondPrize,
                        thirdPrize,
                        activity{
                            name,
                            activityLogo
                        
                            

                        }
                            }
                }

                ''',
        )

        json_post = json.dumps(result.data)

        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def update_event(request, event_id):
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        event_instance = Event.objects.get(id=event_id)
        event_instance.name = python_data["name"]
        event_instance.activity_mode = python_data["activityMode"]
        event_instance.start_date = python_data["startDate"]
        event_instance.end_date = python_data["endDate"]
        event_instance.start_time = python_data["startTime"]
        event_instance.end_time = python_data["endTime"]
        event_instance.max_teams = python_data["maxTeams"]
        event_instance.max_members = python_data["maxMembers"]
        event_instance.first_prize = python_data["firstPrize"]
        event_instance.second_prize = python_data["secondPrize"]
        event_instance.third_prize = python_data["thirdPrize"]

        activity_instance = Activity.objects.get(
            name=python_data["activityName"])
        event_instance.activity = activity_instance
        event_instance.save()

        return HttpResponse({"msg": "successful"}, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def delete_event(request, event_id):
    if request.method == 'DELETE':

        ev = Event.objects.get(id=event_id)
        ev.delete()
    return HttpResponse(200)


def register(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        result = schema.execute(
            '''
            mutation createRegistration($eventId : ID!,$teamId: ID!){
               createRegistration(eventId:$eventId,teamId:$teamId){
                    reg{
                        id
                    }
                }

            }


            ''', variables={'eventId': python_data["event_id"], 'teamId': python_data["team_id"]}
        )

        json_post = json.dumps(result.data)
        size = Team.objects.get(id=python_data["team_id"]).current_size
        event = Event.objects.get(id=python_data["event_id"])
        event.cur_participation = event.cur_participation+size
        event.save()
        print(event.cur_participation)

        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


# get all registrations for a event
def get_all_registrations(request, event_id):
    if request.method == 'GET':
        result = schema.execute(
            '''
            query{
                allRegistrations{
                    event{
                        id
                    },
                    team{
                        id,
                        name
                    }
                }
            }
            ''',
        )

        all_teams = []
        for regs in result.data["allRegistrations"]:
            e_id = int(regs["event"]["id"])
            if e_id == event_id:
                all_teams.append(regs["team"])

        json_response = json.dumps(all_teams)
        return HttpResponse(json_response, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


# update team score and players score
def update_score(request):
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        result = schema.execute(
            '''
            mutation updateTeamScores($eventId:ID!,$firstPrizeTeamId:ID!,$secondPrizeTeamId:ID!,$thirdPrizeTeamId:ID!){
                updateTeamScores(eventId:$eventId,firstPrizeTeamId:$firstPrizeTeamId,secondPrizeTeamId:$secondPrizeTeamId,thirdPrizeTeamId:$thirdPrizeTeamId){
                    event{
                        id
                    }
                }
            }
            ''', variables={'eventId': python_data['event_id'], 'firstPrizeTeamId': python_data['first_prize_team_id'], 'secondPrizeTeamId': python_data['second_prize_team_id'], 'thirdPrizeTeamId': python_data['third_prize_team_id']}
        )

        print(result)
        json_response = json.dumps(result.data)
        return HttpResponse(json_response, content_type="application/json")
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_rank_by_activity(request, activity_id):
    if request.method == 'GET':
        players = Player.objects.filter(
            activity_id=activity_id).values("user_id").annotate(total_score=Sum('score')).order_by("-total_score")

        result = []
        for user in players:
            usr = User.objects.get(id=user['user_id'])
            result.append({"name": usr.first_name+" " +
                           usr.last_name, "score": user['total_score']})
        print(result[0:20])

        json_response = json.dumps(result[0:20])
        return HttpResponse(json_response, content_type="application/json")
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_overall_rank(request):
    if request.method == 'GET':
        players = Player.objects.values("user_id").annotate(
            total_score=Sum('score')).order_by("-total_score")

        result = []
        # users = Player.objects.all().order_by("-score")

        # mydict = {'username': "Ayush Mishra", "event": "Event-1"}
        # html_template = 'success.html'
        # html_message = render_to_string(html_template, context=mydict)
        # subject = 'Thank you for Registering'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ['ayushmishra7@deloitte.com', 'm.ayush089@gmail.com']
        # message = EmailMessage(subject, html_message,
        #                        email_from, recipient_list)
        # message.content_subtype = 'html'
        # message.send()

        for user in players:
            usr = User.objects.get(id=user['user_id'])
            result.append({"name": usr.first_name+" " +
                           usr.last_name, "score": user['total_score']})

        print(result[0:20])
        json_response = json.dumps(result[0:20])
        return HttpResponse(json_response, content_type="application/json")
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_hottest_challenge(request):
    if request.method == 'GET':
        registrations = Registration.objects.values("event_id").annotate(
            no_of_teams=Count('team_id')).order_by("-no_of_teams")
        print(registrations)
        hot_challenge = ""
        for registration in registrations:
            event_id = registration['event_id']
            print(event_id)
            event = Event.objects.get(id=event_id)
            print(event.status)
            if event.status == 'Active':
                hot_challenge = event
                break
        if hot_challenge != "":
            hot_challenge = {'event': hot_challenge.name}
            return HttpResponse(json.dumps(hot_challenge), content_type='application/json')
        else:
            hot_challenge = {'event': "hottest challenge not available"}
            return HttpResponse(json.dumps(hot_challenge), content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_top_performer(request):
    if request.method == 'GET':
        players = Player.objects.values("user_id").annotate(
            total_score=Sum('score')).order_by("-total_score")
        top_player_id = players[0]['user_id']
        top_player = User.objects.get(id=top_player_id)
        top_player = {"name": top_player.first_name+" "+top_player.last_name}
        return HttpResponse(json.dumps(top_player), content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_star_of_week(request):
    if request.method == "GET":

        events = Event.objects.all()

        # print(datetime.datetime.now())
        score = 0
        star = ""
        for event in events:
            # print(event.created_on.astimezone())
            curr = datetime.datetime.now().astimezone()
            diff = event.created_on.astimezone()

            res = curr-diff

            print(res.days)
            if (res.days <= 7):
                result = schema.execute(
                    '''
                    query{
                        allRegistrations{
                            event{
                                id
                            },
                            team{
                                id,
                                name
                            }
                        }
                    }
                    ''',
                )

                all_teams = []
                for regs in result.data["allRegistrations"]:
                    e_id = int(regs["event"]["id"])
                    if e_id == event.pk:
                        all_teams.append(regs["team"])

                for team in all_teams:
                    players = Player.team.through.objects.filter(
                        team_id=team["id"])
                    for player in players:
                        plr = Player.objects.get(id=player.player_id)
                        if plr.score >= score:
                            score = plr.score
                            user = User.objects.get(id=plr.user_id)
                            star = ""+user.first_name+" "+user.last_name

        response = {"name": star, "score": score}
        json_response = json.dumps(response)

        return HttpResponse(json_response, content_type='application/json')


def get_events_participated(request, user_id):
    if request.method == "GET":
        events = Event.objects.all()
        total = events.__len__()
        print(total)
        count = 0
        for event in events:

            result = schema.execute(
                '''
                    query{
                        allRegistrations{
                            event{
                                id
                            },
                            team{
                                id,
                                name
                            }
                        }
                    }
                    ''',
            )

            all_teams = []
            for regs in result.data["allRegistrations"]:
                e_id = int(regs["event"]["id"])
                if e_id == event.pk:
                    all_teams.append(regs["team"])

            for team in all_teams:
                players = Player.team.through.objects.filter(
                    team_id=team["id"])
                for player in players:
                    plr = Player.objects.get(id=player.player_id)
                    if plr.user_id == user_id:
                        count += 1

        response = {"total_events": total, "participated": count}
        json_response = json.dumps(response)

        return HttpResponse(json_response, content_type='application/json')


def get_my_rank(request, user_id):
    if request.method == 'GET':
        players = Player.objects.values("user_id").annotate(
            total_score=Sum('score')).order_by("-total_score")

        result = []

        for user in players:
            usr = User.objects.get(id=user['user_id'])
            result.append(user['user_id'])

        myRank = result.index(user_id)

        json_response = json.dumps({"myrank": myRank+1})
        return HttpResponse(json_response, content_type="application/json")
    else:
        return HttpResponse("wrong request", content_type='application/json')
