from django.shortcuts import render
import io
from django.http import HttpResponse
import json
from rest_framework.parsers import JSONParser
from .schema import schema
from .models import Detail, Question

# Create your views here.


def create_detail(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # print(python_data["name"])

        result = schema.execute(
            '''
            mutation create_detail($theme: String!, $bgImage: String!, $numberOfQuestions: Int!, $level: Int!){
            createDetail(theme: $theme, bgImage: $bgImage, numberOfQuestions:$numberOfQuestions, level:$level){
                escapeRoomDetails
                {
                id
                }
            }
            }
            ''', variables={'theme': python_data["theme"], 'bgImage': python_data["bgImage"], 'numberOfQuestions': python_data["numberOfQuestions"], 'level': python_data["level"]}
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
            mutation update_detail($id:ID!,$theme: String!, $bgImage: String!, $numberOfQuestions: Int!, $level: Int!){
                updateDetail(id:$id,theme: $theme, bgImage: $bgImage, numberOfQuestions:$numberOfQuestions, level:$level){
                    escapeRoomDetails {
                        id
                    }
                }
            }
            ''', variables={'id': room_id, 'theme': python_data["theme"], 'bgImage': python_data["bgImage"], 'numberOfQuestions': python_data["numberOfQuestions"], 'level': python_data["level"]}
        )
        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)


def get_all_rooms(request):
    if request.method == "GET":
        response = [item.theme for item in Detail.objects.all()]
        json_post = json.dumps(response)
        return HttpResponse(json_post, content_type='application/json')


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


def get_all_questions(request):
    if request.method == "GET":
        response = [item.question for item in Question.objects.all()]
        json_post = json.dumps(response)
        return HttpResponse(json_post, content_type='application/json')


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
                mutation update_question($id:Int!,$escapeRoomTheme: String!, $context: String!, $numberOfImages: Int!, $images: String!,$options:String!,$questionType:Int!,$question:String!,$answers:String!,$hints:String!){
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
