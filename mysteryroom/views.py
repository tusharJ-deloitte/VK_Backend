from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
import json

def service_check(request):
    return HttpResponse("Mystery Room Service up and running...",content_type="application/json",status=200)
