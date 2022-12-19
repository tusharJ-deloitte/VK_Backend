from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_posts/<int:pk>', views.get_posts, name='get_posts'),
    path('get_category/<int:pk>', views.get_category, name='get_category'),
    path('create_category', views.create_category, name='create_category'),
    path('update_category/<int:pk>', views.update_category, name="update_category"),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category')
]