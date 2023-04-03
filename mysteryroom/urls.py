from django.urls import path
from .views import *

urlpatterns = [
    path('check/', service_check, name="Mystery Room Service Check"),
    path('collection/create', create_collection, name="create collection"),
    path('collection/edit', edit_collection, name="edit_collection"),
    path('collection/delete/<int:collection_id>',delete_collection, name="delete_collection"),
    path('collection/get/<int:collection_id>',
         get_collection, name="get_collection"),
    path('collection/all', get_all_collections, name="get_all_collections"),
    path('collection/publish', publish_collection, name="publish_collection"),

    path('room/create', create_room, name="create_room"),
    path('room/edit', edit_room, name="edit_room"),
    path('room/delete/<int:room_id>', delete_room, name="delete_room"),
    path('room/get/<int:collection_id>/<int:room_id>', get_room, name="get_room"),
    path('room/all/<int:collection_id>', get_all_rooms, name="get_all_rooms"),

    path('room/question/add', add_question, name="add_question"),
    path('room/question/add_new', add_new_question, name="add_new_question"),
    path('room/question/edit', edit_question, name="edit_question"),
    path('room/question/delete/<int:collection_id>/<int:room_id>/<int:question_number>',
         delete_question, name="delete_question"),
    path('room/question/<int:collection_id>/<int:room_id>/<int:question_number>',
         get_particular_question, name="get_particular_question")

]