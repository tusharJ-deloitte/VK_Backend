from django.shortcuts import render
from .models import Activity
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import io
from rest_framework.parsers import JSONParser
from .schema import schema
import json


def home(request):
    return render(request, 'app1/home.html')

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
            '''
            , variables = {'name': python_data["name"],'category':python_data["category"],'teamSize':python_data["teamSize"]}
        )

        print("------------------------")
        print("final result : ",  result)

        json_post = json.dumps(result.data)

    return HttpResponse(json_post, content_type='application/json')

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
            '''
            , variables = {'id' : pk, 'name': python_data["name"],'categoryId':python_data['categoryId'],'teamSize':python_data['teamSize']}
        )

        print("------------------------")
        print("final result : ",  result)

        json_post = json.dumps(result.data)

    return HttpResponse(json_post, content_type='application/json')

def get_activity(request,pk):
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
            '''
            , variables = {'id': pk}
        )

        json_post = json.dumps(result.data)

    return HttpResponse(json_post, content_type='application/json')

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
            '''
            , variables = {'id' : pk}
        )

        print("------------------------")
        print("final result : ",  result)

        return HttpResponse(status=200)
    return HttpResponse(status=200)

def create_teams(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        
        result = schema.execute(
            '''
            mutation createTeams($name : String!,$activity: String!,$currentSize:Int!,$teamLead:String!){
               createTeam(name:$name,activity:$activity,teamLead:$teamLead,currentSize:$currentSize){
                    team{
                        id
                    }
                }     
  
            }

            '''
            , variables = {'name': python_data["name"],'activity':python_data["activity"],'currentSize':python_data["currentSize"],'teamLead':python_data["teamLead"]}
        )
        
        for item in range(0,python_data["currentSize"]):
                username = python_data['members'][item]
                result1 = schema.execute(
                        '''
                        mutation createPlayer($teamName:String!,$userName:String!,$score:Int!,$activity:String!){
                            createPlayer(teamName:$teamName,username:$userName,score:$score,activity:$activity){
                                player{
                                    id
                                    score
                                }
                            }
                        }
                        '''
                        , variables = {'teamName': python_data["name"],'activity':python_data["activity"],'userName':username,'score':0}
                    )

        json_post = json.dumps(result.data)

    return HttpResponse(json_post, content_type='application/json')

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

