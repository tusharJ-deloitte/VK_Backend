from django.urls import path
from escaperoom import views

urlpatterns = [
    path('create_room', views.create_detail, name="create_room"),
    path('delete_room/<int:room_id>', views.delete_detail, name="delete_room"),
    path('update_room/<int:room_id>', views.update_detail, name="update_detail"),
    path('get_all_rooms', views.get_all_rooms, name="get_all_rooms"),
    path('add_questions', views.add_questions, name="add_questions")
]
