from django.shortcuts import render
import io
from django.http import HttpResponse
import json
from rest_framework.parsers import JSONParser
from .schema import schema

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
            ''', variables={'theme': python_data["theme"],'bgImage': python_data["bgImage"], 'numberOfQuestions': python_data["numberOfQuestions"], 'level': python_data["level"]}
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
