from django.shortcuts import render
<<<<<<< HEAD
from .models import Post
from .serializers import PostSerializer, CategorySerializer
=======
from app1.models import Post
from app1.serializers import PostSerializer
>>>>>>> Balaji
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import io
from rest_framework.parsers import JSONParser
from .schema import schema
import json

def home(request):
    return render(request, 'app1/home.html')

def get_posts(request, pk):
    post = Post.objects.get(id=pk)
    print("----------------------------------")

    print("post : ",post)
    ser = PostSerializer(post)
    print("----------------------------------")

    print("ser : ",ser)
    json_post = JSONRenderer().render(ser.data)
    print("----------------------------------")
     
    print("json_post : ",json_post)

    return HttpResponse(json_post, content_type='application/json')

    # equivalent of JSONRenderer and HTTPResponse combined
    # return JsonResponse(ser.data)
    
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
            '''
            , variables = {'id': pk}
        )

        json_post = json.dumps(result.data)

    return HttpResponse(json_post, content_type='application/json')


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
            '''
            , variables = {'name': python_data["name"]}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)

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
            '''
            , variables = {'id' : pk, 'name': python_data["name"]}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)


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
            '''
            , variables = {'id' : pk}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)


