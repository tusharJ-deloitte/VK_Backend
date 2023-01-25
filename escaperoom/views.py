from django.shortcuts import render
import io
from django.http import HttpResponse
import json
from rest_framework.parsers import JSONParser
from .schema import schema
from app1.models import Event
from .models import Detail, Question, Tally
from heapq import nlargest
from collections import Counter, OrderedDict

# Create your views here.


def create_detail(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # print(python_data["name"])

        result = schema.execute(
            '''
            mutation create_detail($theme: String!,$eventId: Int!, $time: Int!,$bgImage: String!, $numberOfQuestions: Int!, $level: Int!){
            createDetail(theme: $theme, eventId: $eventId, time:$time,bgImage: $bgImage, numberOfQuestions:$numberOfQuestions, level:$level){
                escapeRoomDetails
                {
                id
                }
            }
            }
            ''', variables={'theme': python_data["theme"], 'eventId' :python_data["eventId"], 'time': python_data["time"],'bgImage': python_data["bgImage"], 'numberOfQuestions': python_data["numberOfQuestions"], 'level': python_data["level"]}
        )

        print("------------------------")
        print("final result : ",  result)
        json_post = json.dumps(result.data)
    return HttpResponse(json_post, content_type='application/json')


def delete_detail(request, room_id):
    if request.method == 'DELETE':
        result = schema.execute(
            '''
            mutation delete_detail ($id : ID!){
                deleteDetail (id : $id) {
                    escapeRoomDetails {
                        id
                    }
                }
            }
            ''', variables={'id': room_id}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)


def update_detail(request, room_id):
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        result = schema.execute(
            '''
            mutation update_detail($id:ID!, $eventId: Int!, $time: Int!,$theme: String!, $bgImage: String!, $numberOfQuestions: Int!, $level: Int!){
                updateDetail(id:$id, eventId:$eventId, time:$time,theme: $theme, bgImage: $bgImage, numberOfQuestions:$numberOfQuestions, level:$level){
                    escapeRoomDetails {
                        id
                    }
                }
            }
            ''', variables={'id': room_id, 'theme': python_data["theme"], 'eventId' :python_data["eventId"], 'time': python_data["time"],'bgImage': python_data["bgImage"], 'numberOfQuestions': python_data["numberOfQuestions"], 'level': python_data["level"]}
        )
        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)


# def get_all_rooms(request):
#     if request.method == "GET":
#         response = [item.theme for item in Detail.objects.all()]
#         json_post = json.dumps(response)
#         return HttpResponse(json_post, content_type='application/json')


def add_questions(request, room_id):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        escapeRoomTheme = Detail.objects.get(id=room_id).theme
        for item in python_data:
            result = schema.execute(
                '''
            mutation create_question($escapeRoomTheme: String!, $context: String!, $numberOfImages: Int!, $images: String!,$options:String!,$questionType:Int!,$question:String!,$answers:String!,$hints:String!){
            createQuestion(escapeRoomTheme: $escapeRoomTheme, context: $context, numberOfImages:$numberOfImages, images:$images,options:$options,questionType:$questionType,question:$question,answers:$answers,hints:$hints){
                question
                {
                id
                }
            }
            }
            ''', variables={'escapeRoomTheme': escapeRoomTheme, 'context': item["context"], 'numberOfImages': item["numberOfImages"], 'images': item["images"], 'options': item["options"], 'questionType': item["questionType"], 'question': item["question"], 'answers': item["answers"], 'hints': item["hints"]}
            )
            print("------------------------")
            print("final result : ",  result)

        return HttpResponse(status=200)
    # return HttpResponse(status=200)


# def get_all_questions(request):
#     if request.method == "GET":
#         response = [item.question for item in Question.objects.all()]
#         json_post = json.dumps(response)
#         return HttpResponse(json_post, content_type='application/json')


def update_questions(request, room_id):
    if request.method == "PUT":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        escapeRoomTheme = Detail.objects.get(id=room_id).theme

        existing_questions = []
        questions_list = Question.objects.filter(escape_room_id=room_id)
        for item in questions_list:
            existing_questions.append(item.question)

        d = {}
        for ques in existing_questions:
            d[ques] = -1
        updated_questions = []
        index = {}
        k = 0
        for item in python_data:
            updated_questions.append(item['question'])
            index[item['question']] = k
            k = k+1

        for ques in updated_questions:
            if ques in d.keys():
                d[ques] = d[ques]+1
            else:
                d[ques] = 1

        item = 0
        for ques, value in d.items():
            if value == 1:
                item = index[ques]
                print(item)
                result = schema.execute(
                    '''
                mutation create_question($escapeRoomTheme: String!, $context: String!, $numberOfImages: Int!, $images: String!,$options:String!,$questionType:Int!,$question:String!,$answers:String!,$hints:String!){
                createQuestion(escapeRoomTheme: $escapeRoomTheme, context: $context, numberOfImages:$numberOfImages, images:$images,options:$options,questionType:$questionType,question:$question,answers:$answers,hints:$hints){
                    question
                    {
                    id
                    }
                }
                }
                ''', variables={'escapeRoomTheme': escapeRoomTheme, 'context': python_data[item]["context"], 'numberOfImages': python_data[item]["numberOfImages"], 'images': python_data[item]["images"], 'options': python_data[item]["options"], 'questionType': python_data[item]["questionType"], 'question': ques, 'answers': python_data[item]["answers"], 'hints': python_data[item]["hints"]}
                )
                print("created", ques)
            elif value == -1:
                Question.objects.get(question=ques).delete()
                print("deleted", ques)
            elif value == 0:
                item = index[ques]
                print("item----", item)
                print(python_data[item])
                print(python_data[item]["context"])
                id = Question.objects.get(question=ques).id
                print("id----", id)
                result = schema.execute(
                    '''
                mutation update_question($id:ID!,$escapeRoomTheme: String!, $context: String!, $numberOfImages: Int!, $images: String!,$options:String!,$questionType:Int!,$question:String!,$answers:String!,$hints:String!){
                updateQuestion(id:$id,escapeRoomTheme: $escapeRoomTheme, context: $context, numberOfImages:$numberOfImages, images:$images,options:$options,questionType:$questionType,question:$question,answers:$answers,hints:$hints){
                    question
                    {
                    id
                    }
                }
                }
                ''', variables={'id': id, 'escapeRoomTheme': escapeRoomTheme, 'context': python_data[item]["context"], 'numberOfImages': python_data[item]["numberOfImages"], 'images': python_data[item]["images"], 'options': python_data[item]["options"], 'questionType': python_data[item]["questionType"], 'question': ques, 'answers': python_data[item]["answers"], 'hints': python_data[item]["hints"]}
                )
                print("updated", ques)

        return HttpResponse(200)

def add_scores(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # print(python_data["name"])

        result = schema.execute(
            '''
            mutation create_tally( $teamId: Int!, $eventId: Int!, $finalScore: Int!, $timeTaken: Int!){
            createTally(teamId: $teamId, eventId: $eventId, finalScore:$finalScore,timeTaken: $timeTaken){
                tallyDetails
                {
                id
                }
            }
            }
            ''', variables={'teamId': python_data["teamId"], 'eventId' :python_data["eventId"], 'finalScore': python_data["finalScore"],'timeTaken': python_data["timeTaken"]}
        )

        print("------------------------")
        print("final result : ",  result)
        json_post = json.dumps(result.data)
        return HttpResponse(json_post, content_type='application/json')

def get_all_rooms(request):
    if request.method == 'GET':
        result = schema.execute(
        '''query{
            allDetails{
            id,
            theme,
            event {
            id,
            name,
            activityMode,
            startTime,
            endTime,
            startDate,
            endDate
            }
            bgImage,
            numberOfQuestions,
            time,
            level
        }

        }

                ''',
        )

        json_post = json.dumps(result.data)

        return HttpResponse(json_post, content_type='application/json')

def get_all_questions(request, room_id):
    print("inside get all questions")
    if request.method == 'GET':
        result = schema.execute(
            '''
            query{
            allQuestions{
            escapeRoom{
                id
                event{
                id
                name
                }
                theme
                bgImage
                numberOfQuestions
                time
                level
            }
            id
            context
            numberOfImages
            images
            questionType
            question
            options
            answers
            hints
            }

            }
            ''',
        )

        all_questions=[]
        for question in result.data["allQuestions"]:
            r_id = int(question["escapeRoom"]["id"])
            if r_id == room_id:
                all_questions.append(question)

        json_response = json.dumps(all_questions)
        return HttpResponse(json_response, content_type='application/json')

def get_winner(request, event_id):
    if request.method == 'GET':
        teams = list(Tally.objects.filter(event_id = event_id))
        print(teams)
        winners =[]
        for i in range(0,3):
            greatest = teams[0]
            for j in range(0,len(teams)):
                if(teams[j].final_score > greatest.final_score):
                    greatest = teams[j]
                elif(teams[j].final_score == greatest.final_score):
                    if(teams[j].time_taken < greatest.time_taken):
                        greatest = teams[j]
            winners.append(greatest.team_id)
            teams.pop(teams.index(greatest))    
        print(winners)
        return HttpResponse(200)
    return HttpResponse(200)
            