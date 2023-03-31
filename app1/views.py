from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from .messages import messages
from .models import Detail, Activity, Player, Team, Category, Event, Registration, Pod, IndRegistration, Upload, Notifications, Quiz, QuizQuestion, Option, UserAnswer
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import io
import requests
from GrapheneTest import settings
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
from django.db.models import Sum, Count
import datetime
import boto3
import re
import datetime


from websocket import create_connection
try:
    ws = create_connection(
        "wss://8u1oqx7th4.execute-api.us-east-1.amazonaws.com/production?email=backend@gmail.com")
    print("Connected to web socket successfully")
except:
    print("WebSocket connection unsuccessfull")


def home(request):
    return render(request, 'app1/home.html')


def sns(receiver, subject, message):
    try:
        receiver = receiver
        subject = subject
        message = message
        topic_name = re.split(r'[.@]', receiver)[0]
        print(topic_name)
        sns = boto3.client("sns")
        print(sns)

        # topic_arn = 'arn:aws:sns:us-east-1:458178772538:virtualkunakidza'

        response = sns.create_topic(Name=topic_name)
        print(response)
        topic_arn = response["TopicArn"]
        print(topic_arn)

        response = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscriptions = response["Subscriptions"]
        print(subscriptions)

        if len(subscriptions) == 0:
            print("inside1")
            response = sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=receiver
            )
            return False
            # return HttpResponse(json.dumps({'body': 'User is not subscribed, So user have to manually subscribe to the service.'}), content_type="application/json")
        elif subscriptions[0]['Endpoint'] == receiver and subscriptions[0]['SubscriptionArn'] == 'PendingConfirmation':
            print("inside4")
            return False
            # return HttpResponse(json.dumps({'body': 'User is not subscribed, So user have to manually subscribe to the service.'}), content_type="application/json")
        else:
            print("inside3")
            sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject,
                MessageAttributes={
                    'email': {
                        'DataType': 'String',
                        'StringValue': receiver
                    }
                }
            )

            return True

    except Exception as err:
        print(err)


# register user first time
def registerUser(request):
    try:
        if request.method == 'POST':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)

            if "email" in python_data and "name" in python_data:
                username = python_data["email"].split("@")[0]
                lastname = python_data["name"].split(",")[0]
                firstname = python_data["name"].split(",")[1].strip()

                if User.objects.filter(email=python_data["email"]).exists():
                    return HttpResponse("logged in", content_type='application/json', status=200)

                user_instance = User(
                    username=username,
                    email=python_data["email"],
                    last_name=lastname,
                    first_name=firstname
                )
                user_instance.save()
                detail_instance = Detail(
                    user=user_instance,
                    designation="SDE 1"
                )
                detail_instance.save()
                msg = "Subscribe to AWS SNS service to receive emails."
                response = sns(python_data["email"],
                               "Subscribe to AWS SNS Service", msg)
                if response:
                    print("email sent")
                else:
                    print("not subscribed to email service")
                return HttpResponse("regsitered and logged in", content_type='application/json', status=200)
            else:
                raise Exception("data not found")

        else:
            return HttpResponse("wrong request method", content_type='application/json', status=400)

    except Exception as err:
        return HttpResponse(err, content_type='application/json')


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
    try:
        if request.method == 'GET':
            try:
                user = User.objects.get(email=user_email)
                adminUser = {}
                if user.is_superuser:
                    adminUser = {"isAdmin": 1}
                else:
                    adminUser = {"isAdmin": 0}
                json_post = json.dumps(adminUser)
                return HttpResponse(json_post, content_type='application/json')
            except:
                return HttpResponse("Error Occured", content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


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
    try:
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
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_activity(request, pk):
    try:
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
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_activity_list(request):
    try:
        if request.method == 'GET':
            response = [item.name for item in Activity.objects.all()]
            json_post = json.dumps(response)
            return HttpResponse(json_post, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def delete_activity(request, pk):
    try:
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
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def create_teams(request):
    try:
        if request.method == 'POST':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            print("inside create teams")
            print(python_data)
            try:
                name = Team.objects.get(name=python_data['name'])
                return HttpResponse("Team name already exists", content_type='application/json')
            except Team.DoesNotExist:
                print("unique")

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

            print(python_data["currentSize"])

            # team = Team.objects.get(name = python_data["name"])
            # team.team_logo = Te
            newMemberMessageDataForWS, notificationsToBeSent = {}, []
            for item in range(0, python_data["currentSize"]):
                user_email = python_data['players'][item]
                print(user_email)
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

                msg = f"Congratulations! You have been added to the team {python_data['name']} under the activity {python_data['activity']}"

                # create new entry in notifications table for new member added to team
                print(
                    "creating new entry in notifications table for adding a new member to team")
                memberAddedNotification = Notifications(
                    message_type="MEMBER_ADDED",
                    message=msg,
                    for_user=user_email
                )
                memberAddedNotification.save()
                print("created new entry in notifications table")
                notificationsToBeSent.append(user_email)
                newMemberMessageDataForWS = {
                    "message_type": "MEMBER_ADDED",
                    "message": msg
                }

                response = sns(user_email, "Team Created", msg)
                if response:
                    print("email sent")
                else:
                    print("not subscribed to email service")

                # send data over the websocket
                newMemberMessageDataForWS["user"] = notificationsToBeSent
                print("this is data", newMemberMessageDataForWS)
                ws.send(json.dumps({"action": "sendToOne",
                        "msg": newMemberMessageDataForWS}))

                print("done")

            json_post = json.dumps(result.data)
            return HttpResponse(json_post, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def update_teams(request, team_id):
    try:
        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            print(python_data)

            team_instance = Team.objects.get(id=team_id)

            isTeamNameChanged = False
            previousTeamName = ""
            team_instance = Team.objects.get(id=team_id)

            if team_instance.name != python_data['name']:
                isTeamNameChanged = True
                previousTeamName = team_instance.name
                try:
                    name = Team.objects.get(name=python_data['name'])
                    return HttpResponse("Team name already exists", content_type='application/json')
                except Team.DoesNotExist:
                    print("unique")
            team_instance.name = python_data['name']
            team_instance.team_lead = python_data['teamLead']
            team_instance.current_size = python_data['currentSize']
            team_instance.team_logo = python_data["team_logo"]
            team_instance.save()

            # activity_instance = Activity.objects.filter(
            #     name=python_data['activity'])[0]
            # activity_id = activity_instance.pk
            # print(activity_instance)
            # team_instance.activity.add(activity_instance)
            # team_instance.save()

            activity_instance = Activity.objects.filter(
                name=python_data['activity'])[0]
            activity_id = activity_instance.pk
            print(activity_instance)
            team_activity_instance = Team.activity.through.objects.filter(
                team_id=team_id)
            for item in team_activity_instance:
                item.delete()
            team_instance.activity.add(activity_instance)
            team_instance.save()

            players = Player.team.through.objects.filter(team_id=team_id)

            print("------- : ", players)
            existing_players = []

            for player in players:
                existing_players.append(Player.objects.get(
                    id=player.player_id).user.email)

            # print("--------\n", existing_players)

            d = {}

            for player in existing_players:
                d[player] = -1

            for player in python_data["players"]:
                if player in d.keys():
                    d[player] = d[player] + 1
                else:
                    d[player] = 1

            # print("********", d)

            addedMessageDataForWS, addedNotificationToBeSent = {}, []
            removedMessageDataForWS, removedNotificationToBeSent = {}, []
            teamNameChangedMessageDataForWS, teamNameChangeNotificationToBeSent = {}, []
            for key, value in d.items():
                username = User.objects.get(email=key).first_name
                id = User.objects.get(email=key).pk
                print(username, id)

                if value == 1:
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

                            ''', variables={'teamName': python_data["name"], 'userEmail': key, 'score': 0, 'activityId': activity_id}
                    )

                    msg = f"Congratulations! You have been added to the team {python_data['name']} under the activity {python_data['activity']}"
                    # create new entry in notifications table for new member added to team
                    print(
                        "creating new entry in notifications table for adding a new member to team")
                    memberAddedNotification = Notifications(
                        message_type="MEMBER_ADDED",
                        message=msg,
                        for_user=key
                    )
                    # data for ws
                    addedMessageDataForWS = {
                        "message_type": "MEMBER_ADDED",
                        "message": msg
                    }
                    addedNotificationToBeSent.append(key)

                    memberAddedNotification.save()
                    print("created new entry in notifications table")

                    user_email = key

                    response = sns(user_email, "Team Created", msg)
                    if response:
                        print("email sent")
                    else:
                        print("not subscribed to email service")

                elif value == -1:
                    l = []
                    p_id = Player.objects.filter(user_id=id)
                    for item in p_id:
                        l.append(item.pk)

                    t_id = Player.team.through.objects.filter(team_id=team_id)
                    for item in t_id:
                        if item.player_id in l:
                            Player.objects.get(id=item.player_id).delete()

                    msg = f"You are removed from the team {python_data['name']}"

                    # create new entry in notifications table for member removed from team
                    print(
                        "creating new entry in notifications table for member removed from team")
                    memberRemovedNotification = Notifications(
                        message_type="MEMBER_REMOVED",
                        message=msg,
                        for_user=key
                    )
                    # data for ws
                    removedMessageDataForWS = {
                        "message_type": "MEMBER_REMOVED",
                        "message": msg
                    }
                    removedNotificationToBeSent.append(key)
                    memberRemovedNotification.save()
                    print("created new entry in notifications table")

                    user_email = key

                    response = sns(user_email, "Team Removed", msg)
                    if response:
                        print("email sent")
                    else:
                        print("not subscribed to email service")

                elif value == 0 and isTeamNameChanged:
                    msg = f"Your team name is changed from {previousTeamName} to {python_data['name']}"
                    # create new entry in notifications table if there is change in team name only to previous members
                    print(
                        "creating new entry in notifications table for change in team name")
                    teamNameNotification = Notifications(
                        message_type="TEAM_NAME_CHANGED",
                        message=msg,
                        for_user=key
                    )
                    # data for ws
                    teamNameChangedMessageDataForWS = {
                        "message_type": "TEAM_NAME_CHANGED",
                        "message": msg
                    }
                    teamNameChangeNotificationToBeSent.append(key)

                    teamNameNotification.save()
                    print("created new entry in notifications table")

                    user_email = key

                    response = sns(user_email, "Team Name Changed", msg)
                    if response:
                        print("email sent")
                    else:
                        print("not subscribed to email service")

            # send added members data over web socket
            addedMessageDataForWS["user"] = addedNotificationToBeSent
            ws.send(json.dumps(
                {"action": "sendToOne", "msg": addedMessageDataForWS}))

            # send removed members data over web socket
            removedMessageDataForWS["user"] = removedNotificationToBeSent
            ws.send(json.dumps({"action": "sendToOne",
                    "msg": removedMessageDataForWS}))

            # send team name changed data over web socket
            teamNameChangedMessageDataForWS["user"] = teamNameChangeNotificationToBeSent
            ws.send(json.dumps({"action": "sendToOne",
                    "msg": teamNameChangedMessageDataForWS}))

            return HttpResponse({"msg": "successful"}, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def delete_teams(request, team_id):
    try:
        if request.method == 'DELETE':
            pt = Player.team.through.objects.filter(team_id=team_id)

            for item in pt:
                Player.objects.get(id=item.player_id).delete()

            Team.objects.get(id=team_id).delete()
            return HttpResponse(200)
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def manage_teams(request, user_email):
    try:
        if request.method == 'GET':
            user_id = User.objects.get(email=user_email).pk
            players = Player.objects.filter(user_id=user_id)
            print("inside--1")

            teams = []

            for player in players:
                try:
                    print("inside try")
                    teams.append(Player.team.through.objects.get(
                        player_id=player.id).team_id)
                except:
                    print("exception")
                    continue

            # print("teams : ", teams)

            response = []
            print("teams", teams)
            for team in teams:

                print("inside teams", team)
                team_id = team
                team_object = Team.objects.get(id=team_id)
                team_name = team_object.name
                team_lead = team_object.team_lead
                team_size = team_object.current_size

                team_lead = team_object.team_lead
                team_logo = team_object.team_logo

                team_mem_ids = Player.team.through.objects.filter(
                    team_id=team_id)

                # print("team_mem_ids", team_mem_ids)
                team_mem = []
                for id in team_mem_ids:
                    print("inside id", id)
                    user_id = Player.objects.get(id=id.player_id).user_id
                    # print("inside for id : ", user_id)
                    user_object = User.objects.get(id=user_id)
                    first_name = user_object.first_name
                    last_name = user_object.last_name
                    user_email = user_object.email
                    p = {

                        "firstName": first_name,
                        "lastName": last_name,
                        "email": user_email
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
                # #print("team_id", temp_response)
                response.append(temp_response)

            json_post = json.dumps(response)
            return HttpResponse(json_post, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def create_event(request):
    try:
        if request.method != 'POST':
            return HttpResponse("wrong request method", content_type='application/json', status=400)

        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # print(python_data)
        result = {}
        event = Event.objects.filter(name=python_data['name'])
        if len(event) != 0:
            raise Exception("Event already exists!")

        # try:
        #     name = Event.objects.get(name=python_data['name'])
        #     return HttpResponse("Event name already exists", content_type='application/json')
        # except Event.DoesNotExist:
        #     print("unique")

        if "minMembers" in python_data:
            result = schema.execute(
                '''
            mutation createEvent($name : String!,$activityName: String!,$activityMode: String!,$minMembers:Int!,$maxMembers:Int!,$startDate:Date!,$endDate:Date!,$startTime:Time!,$endTime:Time!,$eventType: String!){
                createEvent(name:$name,activityName:$activityName,activityMode:$activityMode,minMembers:$minMembers,maxMembers:$maxMembers,startTime:$startTime,endTime:$endTime,startDate:$startDate,endDate:$endDate,eventType:$eventType){
                    event{
                        id
                        name
                    }   
                }
            }
            ''', variables={'name': python_data["name"], 'activityName': python_data["activityName"], 'activityMode': python_data['activityMode'], 'minMembers': python_data["minMembers"], 'maxMembers': python_data["maxMembers"], 'startDate': python_data['startDate'], 'endDate': python_data['endDate'], 'startTime': python_data['startTime'], 'endTime': python_data['endTime'], 'eventType': python_data["eventType"]}
            )
            result = result.data['createEvent']['event']['id']
        else:
            result = schema.execute(
                '''
            mutation createIndEvent($name : String!,$activityName: String!,$activityMode: String!,$startDate:Date!,$endDate:Date!,$startTime:Time!,$endTime:Time!,$eventType: String!){
                createIndEvent(name:$name,activityName:$activityName,activityMode:$activityMode,startTime:$startTime,endTime:$endTime,startDate:$startDate,endDate:$endDate,eventType:$eventType){
                    event{
                        id
                        name
                    }
                }
            }
            ''', variables={'name': python_data["name"], 'activityName': python_data["activityName"], 'activityMode': python_data['activityMode'], 'startDate': python_data['startDate'], 'endDate': python_data['endDate'], 'startTime': python_data['startTime'], 'endTime': python_data['endTime'], 'eventType': python_data["eventType"]}
            )
            result = result.data['createIndEvent']['event']['id']

        # create new entry in notifications table for new event creation
        print("creating new entry in notifications table")
        msg = f"New Event {python_data['name']} created under {python_data['activityName']} activity. Go and register now!"
        newEventNotification = Notifications(
            message_type="EVENT_CREATED",
            message=msg,
            for_user="ALL"
        )
        newEventNotification.save()
        # send data over the websocket
        ws.send(json.dumps({
            "action": "sendToAll",
            "msg": {
                "message_type": "EVENT_CREATED",
                "message": msg,
            }
        }))
        newEventNotification.save()
        print("created new entry in notifications table")

        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_all_events(request):
    try:
        if request.method == 'GET':
            print("inside get all events")
            result = schema.execute(
                '''query{
                        allEvents{
                            id,
                            createdOn,
                            name,
                            eventType,
                            activityMode,
                            minMembers,
                            maxMembers,
                            curParticipation,
                            startDate,
                            endDate,
                            startTime,
                            endTime,
                            taskId,
                            activity{
                                name                             
                                activityLogo
                                

                            }
                                }
                    }

                    ''',
            )
            print(datetime.date.today())
            active = []
            elapsed = []
            upcoming = []
            events = Event.objects.all()
            for i, event in enumerate(events):
                print(i)
                curr = datetime.date.today()
                curt = datetime.datetime.now().time()
                if event.end_date < curr:
                    event.status = event.ELAPSED
                    event.save()
                    result.data['allEvents'][i]['status'] = "elapsed"
                    elapsed.append(result.data['allEvents'][i])
                elif event.start_date > curr:
                    event.status = event.YET_TO_START
                    event.save()
                    result.data['allEvents'][i]['status'] = "yet to start"
                    upcoming.append(result.data['allEvents'][i])
                elif event.end_time < curt and event.end_date == curr:
                    event.status = event.ELAPSED
                    event.save()
                    result.data['allEvents'][i]['status'] = "elapsed"
                    elapsed.append(result.data['allEvents'][i])
                elif event.start_time > curt and event.start_date == curr:
                    event.status = event.YET_TO_START
                    event.save()
                    result.data['allEvents'][i]['status'] = "yet to start"
                    upcoming.append(result.data['allEvents'][i])
                else:
                    event.status = event.ACTIVE
                    event.save()
                    result.data['allEvents'][i]['status'] = "active"
                    active.append(result.data['allEvents'][i])

            print("outside loop")

            json_post = json.dumps(
                {"active": active, "upcoming": upcoming, "elapsed": elapsed})

            print(len(json_post))

            return HttpResponse(json_post, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def update_event(request, event_id):
    try:

        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)

            if python_data["isNameChanged"] == True:
                # print(python_data)
                try:
                    name = Event.objects.get(name=python_data['name'])
                    return HttpResponse("Event name already exists", content_type='application/json')
                except Event.DoesNotExist:
                    print("unique")

            if python_data['eventType'] == "Group":
                event_instance = Event.objects.get(id=event_id)
                event_instance.name = python_data["name"]
                event_instance.activity_mode = python_data["activityMode"]
                event_instance.start_date = python_data["startDate"]
                event_instance.end_date = python_data["endDate"]
                event_instance.start_time = python_data["startTime"]
                event_instance.end_time = python_data["endTime"]
                event_instance.min_members = python_data["minMembers"]
                event_instance.max_members = python_data["maxMembers"]
                activity_instance = Activity.objects.get(
                    name=python_data["activityName"])
                event_instance.activity = activity_instance
                event_instance.save()
            else:
                event_instance = Event.objects.get(id=event_id)
                event_instance.name = python_data["name"]
                event_instance.activity_mode = python_data["activityMode"]
                event_instance.start_date = python_data["startDate"]
                event_instance.end_date = python_data["endDate"]
                event_instance.start_time = python_data["startTime"]
                event_instance.end_time = python_data["endTime"]
                activity_instance = Activity.objects.get(
                    name=python_data["activityName"])
                event_instance.activity = activity_instance
                event_instance.save()

            return HttpResponse({"msg": "successful"}, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def delete_event(request, event_id):
    try:
        if request.method == 'DELETE':
            ev = Event.objects.get(id=event_id)
            if ev.task_id != 0:
                quiz = Quiz.objects.get(event_id=event_id)
                quiz.event_id = 0
                quiz.save()
            event_id = ev.pk
            if ev.event_type == "Individual":
                player = Player.objects.filter(event_id=event_id)
                for p in player:
                    p.delete()
            else:
                player = Player.objects.filter(event_id=event_id)
                for p in player:
                    p.score = 0
                    p.save()
            ev.delete()
            return HttpResponse({"msg": "successful"}, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def register(request):
    try:
        if request.method != 'POST':
            return HttpResponse("wrong request method", content_type='application/json', status=400)

        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # print(python_data)

        eventInstance = Event.objects.filter(id=python_data['event_id'])
        teamInstance = Team.objects.filter(id=python_data['team_id'])
        print(eventInstance, teamInstance)
        if len(eventInstance) == 0 or len(teamInstance) == 0:
            raise Exception("Event or Team does not exists")
        eventInstance = eventInstance[0]
        teamInstance = teamInstance[0]

        instance = Registration.objects.filter(
            event=eventInstance,
            team=teamInstance
        )
        if len(instance) != 0:
            raise Exception("Team is already registered for the given event!")

        result = schema.execute(
            '''
                mutation createRegistration($eventId : ID!,$teamId: ID!){
                createRegistration(eventId:$eventId,teamId:$teamId){
                        reg{
                            id
                        }
                    }

                }''',
            variables={
                'eventId': python_data["event_id"], 'teamId': python_data["team_id"]}
        )

        json_post = json.dumps(result.data)
        size = teamInstance.current_size
        eventInstance.cur_participation = eventInstance.cur_participation + size
        eventInstance.save()
        # print(eventInstance.cur_participation)

        players = Player.team.through.objects.filter(
            team_id=python_data["team_id"])
        print("players are ----------- ", players)
        notificationToBeSent, participateMessageDataForWS = [], {}
        for player in players:
            user_email = Player.objects.get(id=player.player_id).user.email
            if user_email not in notificationToBeSent:
                # create new entry in notifications table for participation in the event
                print(
                    "creating new entry in notifications table for participation in the event")
                msg = f"Your team {teamInstance.name} has participated in the event {eventInstance.name}"
                participateEventNotification = Notifications(
                    message_type="PARTICIPATE_EVENT",
                    message=msg,
                    for_user=user_email
                )
                participateEventNotification.save()
                notificationToBeSent.append(user_email)
                # data for sending over ws
                participateMessageDataForWS = {
                    "message_type": "PARTICIPATE_EVENT",
                    "message": msg
                }
                print("created new entry in notifications table")

                response = sns(user_email, "Participated in event", msg)
                if response:
                    print("email sent")
                else:
                    print("not subscribed to email service")

        print("list----", notificationToBeSent)
        # send data over the websocket
        participateMessageDataForWS["user"] = notificationToBeSent
        ws.send(json.dumps({
            "action": "sendToOne",
            "msg": participateMessageDataForWS
        }))

        return HttpResponse(json_post, content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def register_individual_user_in_event(request):
    if request.method != 'POST':
        return HttpResponse("wrong request method", content_type='application/json')
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print("individual regisgtration")
        print(python_data)
        eventInstance = Event.objects.filter(id=python_data['event_id'])
        userInstance = User.objects.filter(email=python_data['user_email'])
        print("instances", eventInstance, userInstance)
        if len(eventInstance) == 0 or len(userInstance) == 0:
            raise Exception("Event or user does not exists.")
        eventInstance = eventInstance[0]
        userInstance = userInstance[0]
        activity_id = eventInstance.activity.pk
        # print(activity_id)

        player = Player.objects.filter(
            user=userInstance, event_id=python_data['event_id'])
        if len(player) != 0:
            raise Exception("User already registered for the event.")

        result = schema.execute(
            '''
                mutation createIndPlayer($userEmail:String!,$score:Int!,$activityId:Int!,$eventId:Int!){
                    createIndPlayer(userEmail:$userEmail,score:$score,activityId:$activityId,eventId:$eventId){
                        player{
                            id
                        }
                    }
                }

            ''', variables={'userEmail': python_data['user_email'], 'score': 0, 'activityId': activity_id, 'eventId': python_data['event_id']}
        )

        player_id = result.data['createIndPlayer']['player']['id']
        result2 = schema.execute(
            '''
            mutation createIndRegistration($eventId : ID!,$playerId: ID!){
            createIndRegistration(eventId:$eventId,playerId:$playerId){
                    reg{
                        id
                    }
                }

            }


            ''', variables={'eventId': python_data["event_id"], 'playerId': player_id}
        )
        json_post = json.dumps(result2.data)
        eventInstance.cur_participation = eventInstance.cur_participation + 1
        eventInstance.save()
        print("doneeeeeeeee")
        # create new entry in notifications table for participation in the event
        print("creating new entry in notifications table for participation in the event")
        msg = f"You have participated in the event {eventInstance.name}"
        participateEventNotification = Notifications(
            message_type="PARTICIPATE_EVENT",
            message=msg,
            for_user=python_data['user_email']
        )
        participateEventNotification.save()
        print("created new entry in notifications table")

        # send data over the websocket
        ws.send(json.dumps({
            "action": "sendToOne",
            "msg": {
                "message_type": "PARTICIPATE_EVENT",
                "message": msg,
                "user": [python_data['user_email']]
            }
        }))

        user_email = python_data['user_email']

        response = sns(user_email, "Registered in event", msg)
        if response:
            print("email sent")
        else:
            print("not subscribed to email service")

        return HttpResponse(json_post, content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


# get all registrations for a event
def get_all_registrations(request, event_id):
    try:
        if request.method == 'GET':
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return HttpResponse("wrong request", content_type='application/json')

            all_teams = []
            if event.event_type == "Group":
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
                for regs in result.data["allRegistrations"]:
                    e_id = int(regs["event"]["id"])
                    if e_id == event_id:
                        all_teams.append(regs["team"])
            else:
                result2 = schema.execute(
                    '''
                    query{
                        allIndregistrations{
                            event{
                                id
                            }
                            player{
                                id
                            }
                        }
                    }
                ''',
                )
                for regs in result2.data["allIndregistrations"]:
                    e_id = int(regs["event"]["id"])
                    if e_id == event_id:
                        player = Player.objects.get(id=regs["player"]["id"])
                        all_teams.append(
                            {"id": player.pk, "name": player.user.first_name+" "+player.user.last_name})

            json_response = json.dumps(all_teams)
            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


# update team score and players score
def update_score(request):
    try:
        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            # print(python_data)

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

            # print(result)
            json_response = json.dumps(result.data)
            return HttpResponse(json_response, content_type="application/json")
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_rank_by_activity(request, activity_id):
    try:
        if request.method == 'GET':
            players = Player.objects.filter(
                activity_id=activity_id).values("user_id").annotate(total_score=Sum('score')).order_by("-total_score")

            result = []
            for user in players:
                usr = User.objects.get(id=user['user_id'])
                rating = getMyRating(user['total_score'])
                try:
                    designation = Detail.objects.get(user_id=usr.pk)
                    result.append({"name": usr.first_name+" " +
                                   usr.last_name, "rating": rating, "score": user['total_score'], "designation": designation.designation})
                except Detail.DoesNotExist:
                    result.append({"name": usr.first_name+" " +
                                   usr.last_name, "rating": rating, "score": user['total_score'], "designation": "None"})
            # print(result[0:20])

            json_response = json.dumps(result[0:20])
            return HttpResponse(json_response, content_type="application/json")
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_overall_rank(request):
    try:
        if request.method == 'GET':
            players = Player.objects.values("user_id").annotate(
                total_score=Sum('score')).order_by("-total_score")

            result = []

            for user in players:
                usr = User.objects.get(id=user['user_id'])
                rating = getMyRating(user['total_score'])
                try:
                    designation = Detail.objects.get(user_id=usr.pk)
                    result.append({"name": usr.first_name+" " +
                                   usr.last_name, "rating": rating, "score": user['total_score'], "designation": designation.designation})
                except Detail.DoesNotExist:
                    result.append({"name": usr.first_name+" " +
                                   usr.last_name, "rating": rating, "score": user['total_score'], "designation": "None"})

            json_response = json.dumps(result[0:20])
            return HttpResponse(json_response, content_type="application/json")
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_hottest_challenge(request):
    if request.method != 'GET':
        return HttpResponse("wrong request method", content_type='application/json', status=400)
    try:

        events = Event.objects.all().exclude(
            status=Event.ELAPSED).order_by("-cur_participation")
        if len(events) == 0:
            raise Exception({"message": "no event found!"})

        print(events[0])
        event = events[0]
        result = json.dumps({
            "id": event.pk,
            "event": event.name,
        })
        return HttpResponse(result, content_type='application/json')

    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_top_performer(request):
    try:
        if request.method == 'GET':
            try:
                players = Player.objects.values("user_id").annotate(
                    total_score=Sum('score')).order_by("-total_score")
                top_player_id = players[0]['user_id']
                top_player = User.objects.get(id=top_player_id)
                top_player = {"name": top_player.first_name +
                              " "+top_player.last_name}
                return HttpResponse(json.dumps(top_player), content_type='application/json')
            except:
                return HttpResponse("", content_type='application/json')

        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_star_of_week(request):
    try:
        if request.method == "GET":

            events = Event.objects.all()

            # #print(datetime.datetime.now())
            score = 0
            star = ""
            for event in events:
                # #print(event.created_on.astimezone())
                curr = datetime.date.today()
                diff = event.start_date

                res = curr-diff

                # print(res.days)
                if (res.days <= 7):

                    if event.event_type == "Group":

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
                    else:
                        result = schema.execute(
                            '''
                            query{
                                allIndregistrations{
                                    event{
                                        id
                                    }
                                    player{
                                        id
                                    }
                                }
                            }
                            ''',
                        )
                        for regs in result.data["allIndregistrations"]:
                            e_id = int(regs["event"]["id"])
                            if e_id == event.pk:
                                player = Player.objects.get(
                                    id=regs["player"]["id"])
                                if (player.score >= score):
                                    score = player.score
                                    user = User.objects.get(id=player.user_id)
                                    star = ""+user.first_name+" "+user.last_name

            response = {"name": star, "score": score}
            json_response = json.dumps(response)

            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_events_participated(request, user_email):
    try:
        if request.method != "GET":
            return HttpResponse("wrong request method", content_type='application/json')

        print("finding user with given email ", user_email)
        user_id = User.objects.get(email=user_email).pk
        events = Event.objects.all()
        print("all events::", events)

        not_participated = []
        total = events.__len__()
        results = schema.execute(
            '''query{
                    allEvents{
                        id,
                        status,
                        createdOn,
                        name,
                        eventType,
                        activityMode,
                        minMembers,
                        maxMembers,
                        curParticipation,
                        startDate,
                        endDate,
                        startTime,
                        endTime,
                        activity{
                            name,
                            activityLogo    
                        }
                    }
                }
                ''',)
        all_events = []
        # print(total)
        count = 0
        for i, event in enumerate(events):
            if event.event_type == "Group":
                print("finding group event registrations")
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
                print("result::", result)
                all_teams = []
                for regs in result.data["allRegistrations"]:
                    e_id = int(regs["event"]["id"])
                    if e_id == event.pk:
                        all_teams.append(regs["team"])
                flag = 0
                print("all teams::", all_teams)
                for team in all_teams:
                    players = Player.team.through.objects.filter(
                        team_id=team["id"])
                    print("players", players, not_participated)
                    for player in players:
                        plr = Player.objects.get(id=player.player_id)
                        if plr.user.pk == user_id:
                            all_events.append(results.data['allEvents'][i])
                            count += 1
                            flag = 1
                if flag == 0:
                    not_participated.append(results.data['allEvents'][i])
            else:
                print("finding individual event registrations")
                result = schema.execute(
                    '''
                        query{
                            allIndregistrations{
                                event{
                                    id
                                }
                                player{
                                    id
                                }
                            }
                        }
                        ''',
                )
                flag = 0
                for regs in result.data["allIndregistrations"]:
                    e_id = int(regs["event"]["id"])
                    if e_id == event.pk:
                        player = Player.objects.get(
                            id=int(regs["player"]["id"]))
                        if player.user.pk == user_id:
                            all_events.append(
                                results.data['allEvents'][i])
                            count += 1
                            flag = 1
                if flag == 0:
                    not_participated.append(results.data['allEvents'][i])
        response = {"total_events": total,
                    "participated": count, "events": all_events, "not_participated": not_participated}
        json_response = json.dumps(response)

        return HttpResponse(json_response, content_type='application/json')

    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_my_rank(request, user_email):
    if request.method != 'GET':
        return HttpResponse("wrong request method", content_type='application/json', status=400)
    try:
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception("user not found!")

        user_id = user[0].pk
        players = Player.objects.values("user_id").annotate(
            total_score=Sum('score')).order_by("-total_score")
        print(players)
        count = 0
        found = 0
        for player in players:
            count += 1
            if player['user_id'] == user_id:
                found = 1
                break

        if found == 0 or players[count-1]['total_score'] == 0:
            result = {"myrank": "-"}
        elif count == 1:
            result = {"myrank": "1st"}
        elif count == 2:
            result = {"myrank": "2nd"}
        elif count == 3:
            result = {"myrank": "3rd"}
        else:
            count = str(count)
            result = {"myrank": count+"th"}

        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_top_events_participated(request, user_email):
    try:
        if request.method == "GET":
            user_id = User.objects.get(email=user_email).pk
            players = Player.objects.filter(user_id=user_id).order_by("-score")
            result = []
            for player in players:
                if player.score == 0:
                    continue
                team = Player.team.through.objects.filter(
                    player_id=player.pk)
                if (team.__len__() != 0):
                    reg = Registration.objects.filter(team_id=team[0].team_id)
                    if (reg.__len__() != 0):
                        event = Event.objects.get(id=reg[0].event_id)
                        result.append(
                            {"activity_name": Activity.objects.get(id=event.activity_id).name, "event_name": event.name, "date": str(event.start_date), "score": player.score})
                else:
                    reg = IndRegistration.objects.filter(player_id=player.pk)
                    if (reg.__len__() != 0):
                        event = Event.objects.get(id=reg[0].event_id)
                        result.append(
                            {"activity_name": Activity.objects.get(id=event.activity_id).name, "event_name": event.name, "date": str(event.start_date), "score": player.score})

            json_response = json.dumps(result[0:10])

            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_my_score(request, user_email):
    try:
        if request.method == 'GET':
            user_id = User.objects.get(email=user_email).pk
            try:

                players = Player.objects.filter(user_id=user_id).values("user_id").annotate(
                    total_score=Sum('score')).order_by("-total_score")
                result = {'user_id': user_id,
                          'score': 0, 'rating': 'Bronze-1'}
                if (players.__len__() != 0):
                    res = players[0]
                    # print(res['total_score'])
                    rating = getMyRating(res['total_score'])
                    result = {'user_id': res['user_id'],
                              'score': res['total_score'], 'rating': rating}
                return HttpResponse(json.dumps(result), content_type='application/json')
            except:
                result = {'user_id': user_id,
                          'score': 0, 'rating': 'Bronze-1'}
                return HttpResponse(json.dumps(result), content_type='application/json')

        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_top_events_by_activity(request, user_email, activity_id):
    try:
        if request.method == "GET":
            user_id = User.objects.get(email=user_email).pk
            players = Player.objects.filter(
                user_id=user_id, activity_id=activity_id).order_by("-score")
            result = []
            score = 0
            events = Event.objects.filter(activity_id=activity_id)
            count = 0
            for player in players:
                team = Player.team.through.objects.filter(
                    player_id=player.pk)

                if (team.__len__() != 0):
                    reg = Registration.objects.filter(team_id=team[0].team_id)
                    if (reg.__len__() != 0):
                        event = Event.objects.get(id=reg[0].event_id)
                        count += 1
                        score += player.score
                        result.append(
                            {"activity_name": Activity.objects.get(id=activity_id).name, "event_name": event.name, "date": str(event.start_date), "score": player.score})
                else:
                    reg = IndRegistration.objects.filter(player_id=player.pk)
                    if (reg.__len__() != 0):
                        event = Event.objects.get(id=reg[0].event_id)
                        count += 1
                        score += player.score
                        result.append(
                            {"activity_name": Activity.objects.get(id=event.activity_id).name, "event_name": event.name, "date": str(event.start_date), "score": player.score})

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
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def cancel_registration(request, event_id, user_email):
    if request.method != 'DELETE':
        return HttpResponse("wrong request method.", content_type="application/json", status=400)
    print("inside cancel registration")
    try:
        print("param variables event_id :: ",
              event_id, ", user_email :: ", user_email)
        event = Event.objects.filter(id=event_id)
        user = User.objects.filter(email=user_email)
        if len(event) == 0 or len(user) == 0:
            raise Exception("user or event does not exists!")
        event = event[0]
        user = user[0]

        teamToBeDeleted = None
        if event.event_type == "Group":
            print("searching group registrations")
            registered_teams = Registration.objects.filter(event=event)
            if len(registered_teams) == 0:
                raise Exception("No team registered for the given event.")

            is_registration_found = False
            for team_register in registered_teams:
                team_players = Player.objects.filter(team=team_register.team)
                for player in team_players:
                    if player.user == user:
                        print("team found! deleting registration.")
                        registeration = Registration.objects.get(
                            id=team_register.pk)
                        registeration.delete()
                        print(
                            "registeration deleted! updating current participation of event")
                        event.cur_participation -= team_register.team.current_size
                        event.save()
                        teamToBeDeleted = team_register.team
                        is_registration_found = True
                        break
            if not is_registration_found:
                raise Exception("User is not registered for the event!")
        else:
            print("searching individual registrations")
            users_registration = IndRegistration.objects.filter(event=event)
            is_user_registration_found = False
            for registration in users_registration:
                print("registered user :: ", registration.player.user)
                if registration.player.user == user:
                    print("registration found! deleting registration")
                    IndRegistration.objects.get(id=registration.pk).delete()
                    print("registration deleted! deleting the individual player")
                    Player.objects.get(user=user, event_id=event.pk).delete()
                    print("player deleted! updating current participation of event")
                    event.cur_participation -= 1
                    event.save()
                    is_user_registration_found = True
                    break

            if not is_user_registration_found:
                raise Exception("User is not registered for the event!")

        # sending email to the user
        msg = f"Your registration for event {event.name} is cancelled by {user.first_name}."
        response = sns(user_email, "Cancelled registration", msg)
        if response:
            print("email sent")
        else:
            print("not subscribed to email service")

        # saving and sending notification
        notificationToBeSent = []
        if teamToBeDeleted is not None:
            print("Registered Team :: ", teamToBeDeleted)
            players = Player.objects.filter(team=teamToBeDeleted)
            for player in players:
                notificationToBeSent.append(player.user.email)
        else:
            notificationToBeSent.append(user_email)

        print("notification to be sent :: ", notificationToBeSent)
        for user_mail in notificationToBeSent:
            cancelParticipationNotification = Notifications(
                message_type="CANCEL_PARTICIPATION",
                message=msg,
                for_user=user_mail
            )
            cancelParticipationNotification.save()

        # sending data over web-socket
        ws.send(json.dumps({"action": "sendToOne",
                            "msg": {
                                "message_type": "CANCEL_PARTICIPATION",
                                "message": msg,
                                "user": notificationToBeSent
                            }}))
        return HttpResponse(json.dumps({"message": "Registration cancelled of user for the given event."}), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)


def get_pods(request, user_email):
    try:
        if request.method == "GET":
            print("inside get pods data")
            user = User.objects.get(email=user_email)
            pod_name = Pod.objects.get(user=user).pod_name
            print(pod_name)
            members = [member.user for member in Pod.objects.filter(
                pod_name=pod_name)]
            result = []
            print(members)

            for member in members:
                if member.email == user_email:
                    print("email of logged in user")
                    continue

                designation = Detail.objects.get(user_id=member.pk).designation
                print(designation)
                result.append({
                    "firstName": member.first_name,
                    "lastName": member.last_name,
                    "email": member.email,
                    "detail": {
                        "designation": designation
                    }
                })

            return HttpResponse(json.dumps({"data": result}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({"error": "Wrong Request Method"}), content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")

# Function to get all the users from the organisation


def get_all_users_organisation(request):
    try:
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
                return HttpResponse(json.dumps({"data": allData}), content_type="application/json")
                # return HttpResponse("ok", content_type="application/json")
            except Exception as exception:
                print(exception)
                return HttpResponse(str(exception), content_type='application/json')
        else:
            return HttpResponse("Wrong Request Method", content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def upload_aws(request):
    try:
        if request.method == 'POST':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            print("inside")
            user = User.objects.filter(email=python_data['user_email'])
            if len(user) == 0:
                raise Exception(json.dumps(
                    {"message": "user not found", "status": 400}))
            user = user[0]
            event = Event.objects.filter(name=python_data['event_name'])
            if len(event) == 0:
                raise Exception(json.dumps(
                    {"message": "event not found", "status": 400}))
            event = event[0]
            upload = Upload.objects.filter(
                user=user,
                event=event
            )
            for item in upload:
                print(item.file_name[0:10])
                print(datetime.datetime.now())
                if item.file_name[0:10] == str(datetime.datetime.now()).split(' ')[0]:
                    raise Exception(json.dumps(
                        {"message": "upload already exists", "status": 400}))

            print(str(python_data['file_duration']))
            result = schema.execute(
                '''
                mutation CreateUpload($userEmail:String!,$eventName:String!,$fileDuration:String!,$fileSize:Int!,$uploadedTime:String!){
                    createUpload(userEmail:$userEmail,eventName:$eventName,fileDuration:$fileDuration,fileSize:$fileSize,uploadedTime:$uploadedTime){
                        upload{
                            id
                        }
                    }
                }
                ''', variables={'userEmail': python_data["user_email"], 'eventName': python_data['event_name'], 'fileDuration': python_data['file_duration'], 'fileSize': int(python_data['file_size']), 'uploadedTime': python_data['uploaded_time']})
            print(result)
            id = result.data['createUpload']['upload']['id']
            upload_instance = Upload.objects.get(id=id)
            upload_instance.file_name = str(upload_instance.uploaded_on).split(
                ' ')[0]+python_data['event_name']+python_data["user_email"].split('@')[0]+".mp4"
            print("done---1")
            upload_instance.score = 0
            upload_instance.is_uploaded = True
            upload_instance.save()
            print("done--2")
            msg = f"Uploaded file for event {python_data['event_name']} ."

            response = sns(python_data['user_email'], "Uploaded file", msg)
            if response:
                print("email sent")
            else:
                print("not subscribed to email service")

            return HttpResponse(json.dumps({"data": id}), content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type='application/json')


def delete_file(request, upload_id):
    try:
        if request.method == "DELETE":
            upload_instance = Upload.objects.get(id=upload_id)
            # date=str(upload_instance.uploaded_on).split(' ')[0]
            key = upload_instance.file_name
            print(key)
            print("1")
            # key = date+"___"+upload_instance.event.name+"___"+upload_instance.user.email+"___"+upload_instance.file_name
            s3_client = boto3.client('s3')
            print("2")
            response = s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            print("3")
            print(response)
            upload_instance.delete()
            return HttpResponse("deleted", content_type='application/json')
        else:
            return HttpResponse("wrong request", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


# user flow
def get_list_user_event(request, user_email, event_name):
    try:
        if request.method == "GET":
            response = []
            upload_id = [item for item in Upload.objects.filter(
                user=User.objects.get(email=user_email))]
            for item in upload_id:
                if item.event.name == event_name:
                    response.append(item.pk)

            result = []
            for item in response:
                print(item)
                uploadedOn = Upload.objects.get(id=item).uploaded_on
                result.append({
                    "score": Upload.objects.get(id=item).score,
                    "upload_id": item,
                    "file": settings.CLOUDFRONT_DOMAIN+Upload.objects.get(id=item).file_name,
                    "file_name": Upload.objects.get(id=item).file_name,
                    "uploaded_on_date": str(uploadedOn).split(' ')[0],
                    "uploaded_on_time": Upload.objects.get(id=item).uploaded_time,
                    "is_uploaded": Upload.objects.get(id=item).is_uploaded
                })
            print("outside")

            return HttpResponse(json.dumps({"data": result}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": "Wrong Request Method"}), content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")

# admin flow


def get_uploads(request, event_name):
    try:
        if request.method == "GET":
            upload_id = [item.pk for item in Upload.objects.filter(
                event=Event.objects.get(name=event_name))]
            print(upload_id)
            result = []
            for item in upload_id:
                uploadedOn = Upload.objects.get(id=item).uploaded_on
                print(settings.CLOUDFRONT_DOMAIN +
                      Upload.objects.get(id=item).file_name)
                result.append({
                    "score": Upload.objects.get(id=item).score,
                    "upload_id": item,
                    "user": Upload.objects.get(id=item).user.first_name+" "+Upload.objects.get(id=item).user.last_name,
                    "user_email": Upload.objects.get(id=item).user.email,
                    "file": settings.CLOUDFRONT_DOMAIN+Upload.objects.get(id=item).file_name,
                    "uploaded_on_date": str(uploadedOn).split(' ')[0],
                    "uploaded_on_time": Upload.objects.get(id=item).uploaded_time,
                    "file_name": Upload.objects.get(id=item).file_name,
                    "file_size": Upload.objects.get(id=item).file_size,
                    "file_duration": Upload.objects.get(id=item).file_duration
                })

            return HttpResponse(json.dumps({"data": result}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": "Wrong Request Method"}), content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")

# admin flow


def get_uploads_by_date(request, event_name, date):
    try:
        if request.method == "GET":
            upload_id = [item.pk for item in Upload.objects.filter(
                event=Event.objects.get(name=event_name))]
            print(upload_id)
            result = []
            for item in upload_id:
                uploadedOn = Upload.objects.get(id=item).uploaded_on
                uploaded_on = str(uploadedOn).split(' ')[0]
                if uploaded_on == date:
                    print(settings.CLOUDFRONT_DOMAIN +
                          Upload.objects.get(id=item).file_name)
                    result.append({
                        "score": Upload.objects.get(id=item).score,
                        "upload_id": item,
                        "user": Upload.objects.get(id=item).user.first_name+" "+Upload.objects.get(id=item).user.last_name,
                        "user_email": Upload.objects.get(id=item).user.email,
                        "file": settings.CLOUDFRONT_DOMAIN+Upload.objects.get(id=item).file_name,
                        "uploaded_on_date": str(uploadedOn).split(' ')[0],
                        "uploaded_on_time": Upload.objects.get(id=item).uploaded_time,
                        "file_name": Upload.objects.get(id=item).file_name,
                        "file_size": Upload.objects.get(id=item).file_size,
                        "file_duration": Upload.objects.get(id=item).file_duration
                    })

            print(result)
            return HttpResponse(json.dumps({"data": result}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": "Wrong Request Method"}), content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def plank_update_score(request):
    try:
        if request.method == "POST":
            print("inside plank update score")
            body = request.body
            stream = io.BytesIO(body)
            python_data = JSONParser().parse(stream)

            userInstance = User.objects.filter(email=python_data['user_email'])
            eventInstance = Event.objects.filter(
                name=python_data['event_name'])
            if len(userInstance) == 0 or len(eventInstance) == 0:
                raise Exception("user or event doesn't exists!")
            userInstance = userInstance[0]
            eventInstance = eventInstance[0]

            playerInstance = Player.objects.filter(
                user=userInstance, event_id=eventInstance.pk)
            if len(playerInstance) == 0:
                raise Exception("user is not registered for the event!")
            playerInstance = playerInstance[0]

            uploadInstance = Upload.objects.filter(
                user=userInstance,
                event=eventInstance
            )
            if len(uploadInstance) == 0:
                raise Exception("no video uploaded till now for the event.")

            current_score = int(python_data["score"])
            flag = 0
            for upload in uploadInstance:
                if str(upload.uploaded_on).split(' ')[0] == python_data['date']:
                    # update player score for the leaderboard
                    if upload.score == 0:
                        playerInstance.score = playerInstance.score + current_score
                    else:
                        playerInstance.score = playerInstance.score - upload.score + current_score
                    playerInstance.save()
                    print("player score updated")

                    upload.score = current_score
                    upload.save()

                    flag = 1
                    break

            if flag == 0:
                raise Exception("upload entry not found for the given date.")
            print("score updated for the given upload entry")
            return HttpResponse("score updated for the given upload entry", content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": "Wrong Request Method"}), content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_plank_results_of_event(request, event_id):
    if request.method != 'GET':
        return HttpResponse("Wrong request method", content_type="application/json", status=400)

    try:
        print("inside get plank result of event")
        eventInstance = Event.objects.filter(id=event_id)
        if len(eventInstance) == 0:
            raise Exception("Invalid event ID!")
        event = eventInstance[0]

        uploads = Upload.objects.filter(event=event).values("user").annotate(
            total_score=Sum('score')).order_by("-total_score")
        print(uploads)
        result = []
        for index, upload in enumerate(uploads):
            user = User.objects.get(id=upload['user'])
            details = Detail.objects.get(user=user)
            upload_time = Upload.objects.filter(event=event, user=user)
            total_time = 0
            for ut in upload_time:
                t = ut.file_duration.split(".")[0]
                total_time = total_time + int(t)
            result.append({
                "rank": index+1,
                "name": user.first_name+" "+user.last_name,
                "designation": details.designation,
                "total_score": upload['total_score'],
                "total_time": total_time,
            })

        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def is_uploaded(request):
    try:
        if request.method == "POST":
            body = request.body
            stream = io.BytesIO(body)
            python_data = JSONParser().parse(stream)
            upload_instance = Upload.objects.filter(
                user=User.objects.get(email=python_data['user_email']),
                event=Event.objects.get(name=python_data['event_name'])
            )
            result = []
            print(upload_instance)
            for upload in upload_instance:
                if str(upload.uploaded_on).split(' ')[0] == python_data['date']:
                    uploadedOn = upload.uploaded_on
                    result.append({
                        "score": upload.score,
                        "upload_id": upload.pk,
                        "user": upload.user.first_name+" "+upload.user.last_name,
                        "user_email": upload.user.email,
                        "file": settings.CLOUDFRONT_DOMAIN+upload.file_name,
                        "uploaded_on_date": str(uploadedOn).split(' ')[0],
                        "uploaded_on_time": upload.uploaded_time,
                        "file_name": upload.file_name,
                        "file_size": upload.file_size,
                        "file_duration": upload.file_duration
                    })

                    return HttpResponse(json.dumps({"data": result}), content_type="application/json")

            return HttpResponse(json.dumps({"data": result}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": "Wrong Request Method"}), content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def embed_key(request):
    if request.method == "GET":
        embed_key = "jfKfPfyJRdk"
    return HttpResponse(embed_key)


def get_notifications_of_user(request, user_email):
    try:
        if request.method == 'GET':
            user_notifications = Notifications.objects.filter(
                Q(for_user=user_email) | Q(for_user="ALL")).order_by("-createdOn")
            result = []
            for notification in user_notifications:
                result.append({
                    "message_type": notification.message_type,
                    "message": notification.message,
                    "createdOn": str(notification.createdOn),
                    "seen": notification.seen
                })
            return HttpResponse(json.dumps(result), content_type='application/json', status=400)
        else:
            return HttpResponse("wrong request method", content_type='application/json', status=400)
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type='application/json')


def create_quiz(request):
    try:
        if request.method == 'POST':
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            print(python_data)

            result = schema.execute(
                '''
                mutation createQuiz($title:String!,$image:String!,$description:String!,$numberOfQuestions:Int!,$timeModified:String!){
                    createQuiz(title:$title,image:$image,description:$description,numberOfQuestions:$numberOfQuestions,timeModified:$timeModified){
                        quiz {
                            id
                            title
                            desc
                            timeModified
                        }
                    }
                }
                ''', variables={"title": python_data["title"], "image": python_data["image"], "description": python_data["description"], "numberOfQuestions": python_data['number_of_questions'], "timeModified": python_data['time_modified']}
            )

            if result.errors:
                raise Exception(result.errors[0].message)

            quizData = result.data["createQuiz"]["quiz"]

            return HttpResponse(json.dumps({"message": "quiz saved successfully", "status": 200, "data": quizData}), content_type="application/json")
        else:
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_library_for_quizs(request):
    try:
        if request.method != 'GET':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))

        all_quizs = Quiz.objects.all()
        quizs_information = []
        for quiz in all_quizs:
            all_questions = QuizQuestion.objects.filter(quiz=quiz)
            no_of_questions = len(all_questions)
            total_time = 0
            for question in all_questions:
                total_time = total_time + question.max_timer

            # last_modified = quiz.last_modified
            # last_modified = last_modified.replace(tzinfo=None)
            # time_zone = pytz.timezone('Asia/Kolkata')
            # last_modified = time_zone.localize(last_modified)

            quizs_information.append({
                "quiz_id": quiz.pk,
                "title": quiz.title,
                "event_id": quiz.event_id,
                "number_of_questions_left": quiz.number_of_questions - no_of_questions,
                "event_name": "Quiz not published" if quiz.event_id == 0 else Event.objects.get(id=quiz.event_id).name,
                "event_date": "Quiz not published" if quiz.event_id == 0 else str(Event.objects.get(id=quiz.event_id).start_date),
                "description": quiz.desc,
                "banner_image": quiz.banner_image,
                "last_modified_date": quiz.time_modified.split("=")[0],
                "last_modified_time": quiz.time_modified.split("=")[1],
                "total_questions": quiz.number_of_questions,
                "total_time": total_time
            })
        active = []
        elapsed = []
        for i, item in enumerate(quizs_information):
            curr = datetime.date.today()
            curt = datetime.datetime.now().time()
            print(item)
            if item['event_id'] != 0:
                event = Event.objects.get(name=item['event_name'])
                if event.end_date < curr:
                    elapsed.append(quizs_information[i])
                elif event.end_time < curt and event.end_date == curr:
                    elapsed.append(quizs_information[i])
                else:
                    active.append(quizs_information[i])
            else:
                active.append(quizs_information[i])

        json_post = json.dumps(
            {"active": active, "elapsed": elapsed})
        # print(quizs_information)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_quiz_information(request, quizId):
    try:
        if request.method != 'GET':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))

        quiz = Quiz.objects.filter(id=quizId)
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        print("quiz found")

        all_questions_for_quiz = QuizQuestion.objects.filter(quiz=quiz)
        print(all_questions_for_quiz)
        no_of_questions = len(all_questions_for_quiz)

        questions = []
        total_time = 0

        for question in all_questions_for_quiz:
            print(question)
            all_options_for_question = Option.objects.filter(
                quiz=quiz, question=question)
            options = []
            for option in all_options_for_question:
                options.append({
                    "option_text": option.option_text,
                    "is_correct": option.is_correct
                })

            questions.append({
                "ques_id": question.pk,
                "question_text": question.question_text,
                "question_number": question.question_number,
                "image_clue": question.image_clue,
                "note": question.note,
                "question_type": question.question_type,
                "max_timer": question.max_timer,
                "points": question.points,
                "options": options
            })

            total_time = total_time + question.max_timer

        quiz_information = {
            "quiz_id": quiz.pk,
            "title": quiz.title,
            "event_id": quiz.event_id,
            "number_of_questions_left": quiz.number_of_questions - no_of_questions,
            # "event_name":Event.objects.get(id=quiz.event_id),
            "description": quiz.desc,
            "banner_image": quiz.banner_image,
            "last_modified": quiz.time_modified,
            "total_time": total_time,
            "total_questions": quiz.number_of_questions,
            "questions": questions
        }

        print(quiz_information)
        return HttpResponse(json.dumps(quiz_information), content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def add_user_answer(request):
    try:
        if request.method != 'POST':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))

        body = request.body
        stream = io.BytesIO(body)
        python_data = JSONParser().parse(stream)
        print(python_data)
        user = User.objects.filter(email=python_data['user_email'])
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        quiz = Quiz.objects.filter(id=python_data['quiz_id'])
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        quizQuestion = QuizQuestion.objects.filter(
            id=python_data['question_id'])
        if len(quizQuestion) == 0:
            raise Exception(json.dumps(
                {"message": "question not found", "status": 400}))
        quizQuestion = quizQuestion[0]
        ua = UserAnswer.objects.filter(
            user=user, quiz=quiz, question=quizQuestion)
        if len(ua) != 0:
            raise Exception(json.dumps(
                {"message": "user answer already added for a particular question ", "status": 400}))

        user_answer_instance = UserAnswer(
            user=user,
            quiz=quiz,
            question=quizQuestion,
            submitted_answer=python_data['answer'],  # "ans1,ans2"
            time_taken=python_data['time'],
        )
        user_answer_instance.save()
        if user_answer_instance.question.question_type == "MCQ":
            options = Option.objects.filter(
                question=user_answer_instance.question)
            for option in options:
                if option.option_text == user_answer_instance.submitted_answer and option.is_correct == True:
                    user_answer_instance.is_correct_answer = True
                    user_answer_instance.score = user_answer_instance.question.points
                    user_answer_instance.save()
                    return HttpResponse("user answer is correct", content_type="application/json")
            return HttpResponse("user answer added but incorrect", content_type="application/json")
        else:
            options = Option.objects.filter(
                question=user_answer_instance.question, is_correct=True)
            print(options)
            option_list = [item.option_text for item in options]
            answer_list = user_answer_instance.submitted_answer.split(',')
            print(answer_list)
            if len(option_list) == len(answer_list):
                for item in answer_list:
                    if item not in option_list:
                        return HttpResponse("user answer added but incorrect", content_type="application/json")
                user_answer_instance.is_correct_answer = True
                user_answer_instance.score = user_answer_instance.question.points
            else:
                return HttpResponse("user answer added but incorrect", content_type="application/json")
        user_answer_instance.save()
        return HttpResponse("user answer is correct", content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def score_summary(request):
    try:
        if request.method != 'POST':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))

        body = request.body
        stream = io.BytesIO(body)
        python_data = JSONParser().parse(stream)
        print(python_data)
        user = User.objects.filter(email=python_data['user_email'])
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        quiz = Quiz.objects.filter(id=python_data['quiz_id'])
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        user_answer_instance = UserAnswer.objects.filter(
            user=user,
            quiz=quiz
        )
        correct_answers, total_score, not_attempted, total_time, user_score, user_time = 0, 0, 0, 0, 0, 0
        total_answers = len(user_answer_instance)

        for item in user_answer_instance:
            if item.submitted_answer == "":
                not_attempted = not_attempted+1
            if item.is_correct_answer == True:
                correct_answers = correct_answers+1
                user_score = user_score+item.score
            user_time = user_time+item.time_taken
            total_score = total_score + item.question.points
            total_time = total_time + item.question.max_timer

        result = {}
        result['quiz_name'] = item.quiz.title
        result['attempted'] = total_answers - not_attempted
        result['correct_answers'] = f"{correct_answers}/{total_answers}"
        result['total_answers'] = total_answers
        result['user_time'] = user_time
        result['total_score'] = total_score
        result['user_score'] = user_score
        result['total_time'] = total_time
        print(result)

        # add quiz score to the player
        # player = Player.objects.filter(event_id = quiz.event_id,user=user )
        # if len(player)==0:
        #     raise Exception("player not registered")
        # player=player[0]
        # player.score = user_score
        # player.save()

        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def create_quizquestion(request):
    try:
        if request.method != 'POST':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        result = schema.execute(
            '''
            mutation createQuizQuestion($quiz:Int!,$questionText:String!, $imageClue:String!, $note:String!, $questionType: String!, $maxTimer:Int!, $points: Int!,$questionNumber:Int!){
                createQuizQuestion(quiz:$quiz, questionText:$questionText, imageClue:$imageClue, note:$note, questionType:$questionType, maxTimer:$maxTimer,  points:$points,questionNumber:$questionNumber){
                questionInstance{
                    id                
                }
            }
            }
            ''', variables={'quiz': python_data["quiz"], 'questionText': python_data["questionText"], 'imageClue': python_data["imageClue"], 'note': python_data["note"], 'questionType': python_data["questionType"], 'maxTimer': python_data["maxTimer"], 'points': python_data["points"], 'questionNumber': python_data['questionNumber']}
        )
        print(result.data['createQuizQuestion']['questionInstance']['id'])
        options_list = python_data["options"]
        for item in options_list:
            option_instance = Option(
                quiz=Quiz.objects.get(id=python_data['quiz']),
                question=QuizQuestion.objects.get(
                    id=result.data['createQuizQuestion']['questionInstance']['id']),
                option_text=item[0],
                is_correct=item[1]
            )
            option_instance.save()

        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def edit_quiz(request):
    try:
        if request.method != "POST":
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        quiz = Quiz.objects.filter(id=python_data['quiz_id'])
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        quiz.banner_image = python_data['banner_image']
        quiz.desc = python_data['desc']
        quiz.title = python_data['title']
        quiz.time_modified = python_data['time_modified']
        quiz.save()
        return HttpResponse("edited quiz details", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def delete_quiz(request, quiz_id):
    try:
        if request.method != "DELETE":
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        quiz = Quiz.objects.filter(id=quiz_id)
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        event_id = quiz.event_id
        quiz.delete()
        if event_id != 0:
            ev = Event.objects.filter(id=event_id)
            if len(ev) == 0:
                raise Exception(json.dumps(
                    {"message": "event not found", "status": 400}))
            ev = ev[0]
            ev.task_id = 0
            ev.save()
        return HttpResponse("deleted quiz ", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def add_new_question(request):
    try:
        if request.method != 'POST':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        quiz = Quiz.objects.filter(id=python_data['quiz'])
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        result = schema.execute(
            '''
            mutation createQuizQuestion($quiz:Int!,$questionText:String!, $imageClue:String!, $note:String!, $questionType: String!, $maxTimer:Int!, $points: Int!,$questionNumber:Int!){
                createQuizQuestion(quiz:$quiz, questionText:$questionText, imageClue:$imageClue, note:$note, questionType:$questionType, maxTimer:$maxTimer,  points:$points,questionNumber:$questionNumber){
                questionInstance{
                    id                
                }
            }
            }
            ''', variables={'quiz': python_data["quiz"], 'questionText': python_data["questionText"], 'imageClue': python_data["imageClue"], 'note': python_data["note"], 'questionType': python_data["questionType"], 'maxTimer': python_data["maxTimer"], 'points': python_data["points"], 'questionNumber': python_data['questionNumber']}
        )
        print(result.data['createQuizQuestion']['questionInstance']['id'])
        options_list = python_data["options"]
        for item in options_list:
            option_instance = Option(
                quiz=quiz,
                question=QuizQuestion.objects.get(
                    id=result.data['createQuizQuestion']['questionInstance']['id']),
                option_text=item[0],
                is_correct=item[1]
            )
            option_instance.save()
        quiz.number_of_questions = quiz.number_of_questions + 1
        quiz.save()
        return HttpResponse("added new question", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def delete_quiz_question(request, quiz_id, question_number):
    try:
        if request.method != 'DELETE':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        quiz = Quiz.objects.filter(id=quiz_id)
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        quizQuestion = QuizQuestion.objects.filter(
            quiz=quiz, question_number=question_number)
        print(quizQuestion)
        if len(quizQuestion) == 0:
            raise Exception(json.dumps(
                {"message": "question number not found", "status": 400}))
        question = quizQuestion[0]
        question.delete()
        quiz.number_of_questions = quiz.number_of_questions - 1
        quiz.save()
        quizQuestion2 = QuizQuestion.objects.filter(quiz=quiz)
        for item in quizQuestion2:
            if item.question_number > question_number:
                item.question_number = item.question_number-1
                item.save()

        return HttpResponse("deleted question", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def edit_quiz_question(request):
    try:
        if request.method != 'POST':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        quiz = Quiz.objects.filter(id=python_data['quiz'])
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        quizQuestion = QuizQuestion.objects.filter(
            quiz=quiz, question_number=python_data['questionNumber'])
        if len(quizQuestion) == 0:
            raise Exception(json.dumps(
                {"message": "question number not found", "status": 400}))
        question = quizQuestion[0]
        question.question_text = python_data['questionText']
        question.image_clue = python_data['imageClue']
        question.note = python_data['note']
        question.question_type = python_data['questionType']
        question.max_timer = python_data['maxTimer']
        question.points = python_data['points']
        question.save()

        options_list = python_data["options"]
        options = Option.objects.filter(quiz=quiz, question=question)
        for item in options:
            item.delete()
        for item in options_list:
            option_instance = Option(
                quiz=quiz,
                question=question,
                option_text=item[0],
                is_correct=item[1]
            )
            option_instance.save()

        return HttpResponse("ok", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_particular_question(request, quiz_id, question_number):
    try:
        if request.method != "GET":
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        quiz = Quiz.objects.filter(id=quiz_id)
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not found", "status": 400}))
        quiz = quiz[0]
        quizQuestion = QuizQuestion.objects.filter(
            quiz=quiz, question_number=question_number)
        if len(quizQuestion) == 0:
            raise Exception(json.dumps(
                {"message": "question number not found", "status": 400}))
        question = quizQuestion[0]

        all_options_for_question = Option.objects.filter(
            quiz=Quiz.objects.get(id=quiz_id),
            question=question)
        options = []
        for option in all_options_for_question:
            options.append({
                "option_text": option.option_text,
                "is_correct": option.is_correct
            })
        questions = []
        questions.append({
            "ques_id": question.pk,
            "question_text": question.question_text,
            "question_number": question.question_number,
            "image_clue": question.image_clue,
            "note": question.note,
            "question_type": question.question_type,
            "max_timer": question.max_timer,
            "points": question.points,
            "options": options
        })
        return HttpResponse(json.dumps(questions), content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def publish_quiz_for_event(request):
    try:
        if request.method != 'POST':
            raise Exception(json.dumps(
                {"message": "wrong request method", "status": 400}))
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        event = Event.objects.filter(id=python_data['event_id'])
        if len(event) == 0:
            raise Exception(json.dumps(
                {"message": "event not exists", "status": 400}))
        event = event[0]
        print(event)

        quiz = Quiz.objects.filter(id=python_data['quiz_id'])
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not exists", "status": 400}))
        quiz = quiz[0]
        print("quiz found :: ", quiz)

        if quiz.event_id != 0:
            raise Exception(json.dumps(
                {"message": "quiz already published", "status": 400}))

        event.task_id = quiz.pk
        event.save()

        quiz.event_id = event.pk
        quiz.save()

        return HttpResponse(json.dumps({"message": f"quiz {quiz} published for the event {event}", "status": 200}), content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def is_user_attempted_quiz(request, quiz_id, user_email):
    if request.method != "GET":
        return HttpResponse("wrong request method", content_type="application/json", status=400)
    try:
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception("user does not exist")
        user = user[0]
        quiz = Quiz.objects.filter(id=quiz_id)
        if len(quiz) == 0:
            raise Exception(json.dumps(
                {"message": "quiz not exists", "status": 400}))
        quiz = quiz[0]

        instance = UserAnswer.objects.filter(user=user, quiz=quiz)
        if len(instance) == 0:
            return HttpResponse("user has not attempted the quiz", content_type="application/json")
        return HttpResponse("user has already attempted the quiz", content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json", status=400)


def get_quiz_event_results(request, event_id):
    if request.method != 'GET':
        return HttpResponse("Wrong request method", content_type="application/json", status=400)

    try:
        print("inside get quiz event result ")
        eventInstance = Event.objects.filter(id=event_id)
        if len(eventInstance) == 0:
            raise Exception("Event not exists!")
        event = eventInstance[0]

        if event.activity.name != 'Quiz':
            raise Exception("Event is not a quiz event!")

        quiz_id = event.task_id
        print("quiz id ::", quiz_id)
        if quiz_id == 0:
            raise Exception("Event not published!")

        quiz = Quiz.objects.get(id=quiz_id)
        userAnswers = UserAnswer.objects.filter(quiz=quiz).values('user').annotate(total_score=Sum(
            'score'), total_time=Sum('time_taken')).order_by("-total_score", "total_time")
        print(userAnswers)

        result = []
        previous_score, previous_time = 0, 0
        rank = 0
        for userAnswer in userAnswers:
            user = User.objects.get(id=userAnswer['user'])
            userDetail = Detail.objects.get(user=user)
            if not (userAnswer['total_score'] == previous_score and userAnswer['total_time'] == previous_time):
                rank += 1
            result.append({
                "rank": rank,
                "userId": user.pk,
                "email": user.email,
                "name": user.first_name+" "+user.last_name,
                "designation": userDetail.designation,
                "total_score": userAnswer['total_score'],
                "total_time": userAnswer['total_time']
            })
            previous_score = userAnswer['total_score']
            previous_time = userAnswer['total_time']

        if event.status == event.ELAPSED:
            print("elapsed event, updating player scores")
            for userResult in result:
                rank = userResult['rank']
                if rank > 5:
                    break
                player = Player.objects.get(user=User.objects.get(
                    id=userResult['userId']), event_id=event_id)
                print("player :: ", player, ", rank :: ", rank)
                if player.score != 0:
                    break
                if rank == 1:
                    player.score = 50
                elif rank == 2:
                    player.score = 40
                elif rank == 3:
                    player.score = 30
                elif rank == 4:
                    player.score = 25
                else:
                    player.score = 20
                player.save()
            print("player scores updated!")

        print(result)
        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")
