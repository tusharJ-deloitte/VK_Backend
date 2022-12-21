from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_category/<int:pk>', views.get_category, name='get_category'),
    path('create_category', views.create_category, name='create_category'),
    path('update_category/<int:pk>', views.update_category, name="update_category"),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category'),
    path('create_activity',views.create_activity,name="create_activity"),
    path('update_activity/<int:pk>',views.update_activity,name="update_activity"),
    path('get_activity/<int:pk>',views.get_activity,name="get_activity"),
    path('delete_activity/<int:pk>',views.delete_activity,name="delete_activity"),
    path('create_teams',views.create_teams,name="create_teams")
]