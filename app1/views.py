from django.shortcuts import render
from .models import Detail, Activity, Player, Team, Category, Event, Registration, Upload
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .schema import schema
from django.contrib.auth.models import User
from rest_framework import viewsets
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Sum, Count
from GrapheneTest import settings
import datetime
from GrapheneTest import settings
import boto3
import requests
import base64
import json
import io


def home(request):
    return render(request, 'app1/home.html')


def getMyRating(score):
    if score <= 250:
        if score <= 50:
            return 'Bronze-1'
        elif score <= 100:
            return 'Bronze-2'
        elif score <= 150:
            return 'Bronze-3'
        elif score <= 200:
            return 'Bronze-4'
        elif score <= 250:
            return 'Bronze-5'
    elif score <= 500:
        if score <= 300:
            return 'Silver-1'
        elif score <= 350:
            return 'Silver-2'
        elif score <= 400:
            return 'Silver-3'
        elif score <= 450:
            return 'Silver-4'
        elif score <= 500:
            return 'Silver-5'
    elif score <= 750:
        if score <= 550:
            return 'Gold-1'
        elif score <= 600:
            return 'Gold-2'
        elif score <= 650:
            return 'Gold-3'
        elif score <= 700:
            return 'Gold-4'
        elif score <= 750:
            return 'Gold-5'
    elif score <= 1000:
        if score <= 800:
            return 'Platinum-1'
        elif score <= 850:
            return 'Platinum-2'
        elif score <= 900:
            return 'Platinum-3'
        elif score <= 950:
            return 'Platinum-4'
        elif score <= 1000:
            return 'Platinum-5'
    else:
        return 'Diamond'


def is_admin(request, user_email):
    if request.method == 'GET':
        try:
            user = User.objects.get(email=user_email)
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
        team_activity_instance = Team.activity.through.objects.filter(
            team_id=team_id)
        for item in team_activity_instance:
            item.delete()
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


def manage_teams(request, user_email):
    if request.method == 'GET':
        user_id = User.objects.get(email=user_email).pk
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
            activity = Activity.objects.get(
                id=activity_object[0].activity_id)
            activity_name = activity.name
            activity_size = activity.team_size
            category_id = activity.category_id
            activity_logo = activity.activity_logo
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
        print(ev)
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
            rating = getMyRating(user['total_score'])
            designation = Detail.objects.get(user_id = usr.pk).designation
	        
            result.append({"name": usr.first_name+" " +
                           usr.last_name, "rating": rating, "score": user['total_score'],"designation":designation})
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
            rating = getMyRating(user['total_score'])
            designation = Detail.objects.get(user_id = usr.pk).designation
            result.append({"name": usr.first_name+" " +
                           usr.last_name, "rating": rating, "score": user['total_score'],"designation":designation})

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
            hot_challenge = {'event': ""}
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
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_events_participated(request, user_email):
    if request.method == "GET":
        user_id = User.objects.get(email=user_email).pk
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
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_my_rank(request, user_email):
    if request.method == 'GET':
        user_id = User.objects.get(email=user_email).pk
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


def get_top_events_participated(request, user_email):
    if request.method == "GET":
        user_id = User.objects.get(email=user_email).pk
        players = Player.objects.filter(user_id=user_id).order_by("-score")
        result = []
        for player in players:
            team = Player.team.through.objects.filter(
                player_id=player.pk)
            reg = []
            if (team.__len__() != 0):
                reg = Registration.objects.filter(team_id=team[0].team_id)
            if (reg.__len__() != 0):
                event = Event.objects.get(id=reg[0].event_id)
                result.append(
                    {"activity_name": Activity.objects.get(id=event.activity_id).name, "event_name": event.name, "date": str(event.start_date), "score": player.score})

        json_response = json.dumps(result[0:10])

        return HttpResponse(json_response, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_my_score(request, user_email):
    if request.method == 'GET':
        user_id = User.objects.get(email=user_email).pk
        players = Player.objects.filter(user_id=user_id).values("user_id").annotate(
            total_score=Sum('score')).order_by("-total_score")
        res = {}
        if (players.__len__() != 0):
            res = players[0]
            print(res['total_score'])
            rating = getMyRating(res['total_score'])
            result = {'user_id': res['user_id'],
                      'score': res['total_score'], 'rating': rating}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def get_top_events_by_activity(request, user_email, activity_id):
    if request.method == "GET":
        user_id = User.objects.get(email=user_email).pk
        players = Player.objects.filter(
            user_id=user_id, activity_id=activity_id).order_by("-score")
        result = []
        response = []
        score = 0
        events = Event.objects.filter(activity_id=activity_id)
        count = 0
        for player in players:
            team = Player.team.through.objects.filter(
                player_id=player.pk)
            reg = []
            if (team.__len__() != 0):
                reg = Registration.objects.filter(team_id=team[0].team_id)
            if (reg.__len__() != 0):
                event = Event.objects.get(id=reg[0].event_id)
                count += 1
                score += player.score
                result.append(
                    {"activity_name": Activity.objects.get(id=activity_id).name, "event_name": event.name, "date": str(event.start_date), "score": player.score})

        response = {
            "participation": count,
            "total": events.__len__(),
            "total_score": score,
            "events": result
        }

        json_response = json.dumps(response)

        return HttpResponse(json_response, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')


def upload_aws(request, user_email):
    if request.method == 'POST':
        my_uploaded_file = request.FILES.get('my_uploaded_file')
        # print(type(my_uploaded_file))
        print(my_uploaded_file.name)
        my_uploaded_file.name = str(user_email)+"___"+my_uploaded_file.name
        print(my_uploaded_file.content_type)
        print(my_uploaded_file.size)

        result = schema.execute(
            '''
            mutation CreateUpload($userEmail:String!,$fileName:String!){
                createUpload(userEmail:$userEmail,fileName:$fileName){
                    upload{
                        id
                    }
                }
            }
            ''', variables={'userEmail': user_email, 'fileName': my_uploaded_file.name})

        upload_instance = Upload.objects.get(
            user_id=User.objects.get(email=user_email).id)
        upload_instance.uploaded_file = my_uploaded_file
        upload_instance.save()

        return HttpResponse(200)

# def edit_upload(request,user_email):
#     if request.method == "POST":
#         my_uploaded_file = request.FILES.get('my_uploaded_file')
#         my_uploaded_file.name = str(user_email)+"___"+my_uploaded_file.name

#         upload_instance = Upload.objects.get(user_id = User.objects.get(email = user_email).id)

#         s3_client = boto3.client('s3', region_name=settings.AWS_REGION_NAME)
#         s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=upload_instance.uploaded_file.name)

#         upload_instance.uploaded_file = my_uploaded_file
#         upload_instance.save()
#         return HttpResponse(200)
#     else:
#         return HttpResponse("wrong request", content_type='application/json')


def get_files_list(request):
    if request.method == 'GET':
        response = [settings.CLOUDFRONT_DOMAIN+"/" +
                    item.uploaded_file.name for item in Upload.objects.all()]
        json_post = json.dumps(response)
        return HttpResponse(json_post, content_type='application/json')
    else:
        return HttpResponse("wrong request", content_type='application/json')

# get data from PODS platform
def get_pods_data(request):
    if request.method == 'POST':
        try:
            body = request.body
            stream = io.BytesIO(body)
            data = JSONParser().parse(stream)
            print(data)
            email = data['email']

            # get token to access pods server
            token = get_access_token(
                settings.B2B_TOKEN_URL, settings.B2B_CLIENT_ID, settings.B2B_CLIENT_SECRET)
            print("token :: "+token)

            url = settings.B2B_PODS_URL
            payload = "{\"query\":\"query paginatedAllocationList ($filtering: AllocationListFilterInput) {\\r\\n  paginatedAllocationList(filtering: $filtering) {\\r\\n    result {\\r\\n      pod {\\r\\n        id\\r\\n        podAllocations {\\r\\n          employee {\\r\\n            id\\r\\n            name\\r\\n            email\\r\\n            designation\\r\\n          }\\r\\n          startDate\\r\\n          endDate\\r\\n        }\\r\\n      }\\r\\n    }\\r\\n  }\\r\\n}\",\"variables\":{\"filtering\":{\"employee_Email\":\"" + email + "\",\"startDate_Lte\":\"2023-01-31\",\"endDate_Gte\":\"2023-01-31\"}}}"
            headers = {
                'x-api-token': token,
                'Content-Type': 'application/json'
            }
            print("Sending data request to pods server")
            response = requests.post(url, headers=headers, data=payload)
            print("Response received from PODS")
            if response.status_code != 200:
                print(response.text)
                return HttpResponse(response.text, content_type='application/json',status=response.status_code)

            response = response.json()
            print(response)
            # filtering PODS Data
            pods = response['data']['paginatedAllocationList']['result']
            employee_list = []
            emp_ids = []
            for pod in pods:
                podEmployees = pod['pod']['podAllocations']
                for emp in podEmployees:
                    emp = emp['employee']
                    if emp['id'] in emp_ids or emp['email'] == email:
                        continue
                    emp_ids.append(emp['id'])
                    employee_list.append({
                        "id": emp['id'],
                        "name": emp['name'],
                        "email": emp['email'],
                        "designation": emp['designation']
                    })
            return HttpResponse(json.dumps(employee_list), content_type='application/json')
        except Exception as err:
            print(err)
            return HttpResponse(err, content_type='application/json')
    else:
        return HttpResponse(json.dumps({"error":"Wrong Request Method"}), content_type='application/json',status=400)


# get data from dna platform
def get_all_user_dna(request):
    if request.method == 'GET':
        try:
            print("inside get all users from DNA API")

            # get token to access pods server
            token = get_access_token(
                settings.B2B_TOKEN_URL, settings.B2B_CLIENT_ID, settings.B2B_CLIENT_SECRET)
            print("token :: "+token)

            url = settings.B2B_DASHBOARD_URL
            payload = "{\"query\":\"query allUsers{\\r\\n    listUsers{\\r\\n        result{\\r\\n            id\\r\\n            email\\r\\n            basicProfile{\\r\\n                id\\r\\n                name\\r\\n                profilePic\\r\\n            }\\r\\n            detailedProfile{\\r\\n                designation{\\r\\n                    id\\r\\n                    name\\r\\n                }\\r\\n                doj\\r\\n            }\\r\\n        }\\r\\n    }\\r\\n}\",\"variables\":{}}"
            headers = {
                'x-api-token': token,
                'Content-Type': 'application/json',
                # 'Cookie': 'csrftoken=4UqAWHGIzb3UIeTVU90Ogd05ITUmueZObaV726GSwcV2whtGlndmDuz3Yx5OlXPW'
            }
            print("Sending data request to dashboard server")
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print("data received from server")

            if response.status_code != 200:
                print(response.text)
                return HttpResponse(response.text, content_type='application/json',status=response.status_code)

            response = response.json()
            # Filtering out Users Data
            all_users = response['data']['listUsers']['result']
            users = []
            records_inserted = 0
            for user in all_users:
                name, doj, designation, pic = " ", "2023-02-02", " ", " "
                if user['basicProfile']:
                    if user['basicProfile']['name']:
                        name = user['basicProfile']['name']
                    if user['basicProfile']['profilePic']:
                        pic = user['basicProfile']['profilePic']
                if user['detailedProfile']:
                    if user['detailedProfile']['doj']:
                        doj = user['detailedProfile']['doj']
                    if user['detailedProfile']['designation'] and user['detailedProfile']['designation']['name']:
                        designation = user['detailedProfile']['designation']['name']

                users.append({
                    "id": user['id'],
                    "email": user['email'],
                    "name": name,
                    "designation": designation,
                    "doj": doj,
                    "pic": pic
                })

                print("Saving "+user['email']+" in db.")
                isUser = User.objects.filter(email=user['email'])
                if len(isUser) >= 1:
                    print("User Already exists :: "+user['email'])
                    continue
                elif user['email'] == " " or "@" not in user['email'] or name == " " or designation == " " or doj == "2023-02-02":
                    print("User Not saved :: "+user['email'])
                    continue
                elif " " in name:
                    fname = name.split(' ', 1)[0]
                    lname = name.split(' ', 1)[1]
                else:
                    fname = name
                    lname = " "

                user_instance = User(
                    email=user['email'],
                    username=user['email'].split("@")[0],
                    first_name=fname,
                    last_name=lname
                )
                user_instance.save()
                detail_instance = Detail(
                    user=user_instance,
                    employee_id=user['id'],
                    designation=designation,
                    doj=doj,
                    profile_pic=" "
                )
                detail_instance.save()
                print("User Created :: ", str(user_instance))
                records_inserted = records_inserted + 1

            print(str(records_inserted)+"records inserted into user table")
            return HttpResponse("Done", content_type='application/json')
        except Exception as exception:
            print(exception)
            return HttpResponse(str(exception), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"error":"Wrong Request Method"}), content_type='application/json',status=400)

# function to get the access token from the dna server for b2b query
def get_access_token(token_url, client_id, client_secret):
    try:
        print("inside get_access_token function")
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
        print("sending request for getting access token")
        response = requests.post(token_url, data=data)
        token = response.json()['access_token']
        return token
    except Exception as err:
        raise err


# Function to get all the users from the organisation
def get_all_users_organisation(request):
    if request.method == 'GET':
        try:
            result = schema.execute(
                '''
                    query allUsers{
                        allUsers{
                            firstName
                            lastName
                            email
                            detail{
                                designation
                            }
                        }
                    }
                '''
            )
            allData = result.data['allUsers'][::-1]
            return HttpResponse(json.dumps({"data":allData}),content_type="application/json")
#             return HttpResponse("ok", content_type="application/json")
        except Exception as exception:
            print(exception)
            return HttpResponse(str(exception), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"error":"Wrong Request Method"}), content_type='application/json', status=400)
