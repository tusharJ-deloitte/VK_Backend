from django.urls import path
from escaperoom import views

urlpatterns = [
    path('create_room/', views.create_detail, name="create_room"),
    path('delete_room/<int:room_id>', views.delete_detail, name="delete_room"),

]