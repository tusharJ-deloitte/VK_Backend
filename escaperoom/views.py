from django.shortcuts import render
import io
from django.http import HttpResponse
import json
from rest_framework.parsers import JSONParser
from .schema import schema
from .models import Detail

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


def add_questions(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        number_of_questions = python_data['numberOfQuestions']
        for _ in number_of_questions:
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
            ''', variables={'escapeRoomTheme': python_data["escapeRoomTheme"], 'context': python_data["context"], 'numberOfImages': python_data["numberOfImages"], 'images': python_data["images"], 'options': python_data["options"], 'questionType': python_data["questionType"], 'question': python_data["question"], 'answers': python_data["answers"], 'hints': python_data["hints"]}
            )
            print("------------------------")
            print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)
