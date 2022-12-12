from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse

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

