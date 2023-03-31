from django.urls import path, include
from .views import *

urlpatterns = [
    path('check/', service_check, name="Mystery Room Service Check"),
]
