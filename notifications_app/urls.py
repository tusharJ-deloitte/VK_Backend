from django.urls import path
from notifications_app import views

urlpatterns = [
    path("",views.home,name="home"),
    path("test", views.test, name="test"),
    path("test_celery", views.test_celery, name="test_celery"),
]