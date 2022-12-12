from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_posts/<int:pk>', views.get_posts, name='get_posts')
]