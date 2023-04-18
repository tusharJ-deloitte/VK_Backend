from django.urls import path
from .views import *

urlpatterns = [
    path('check/', service_check, name="Mystery Room Service Check"),
    path('collection/create', create_collection, name="create collection"),
    path('collection/edit', edit_collection, name="edit_collection"),
    path('collection/delete/<int:collection_id>',
         delete_collection, name="delete_collection"),
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
         get_particular_question, name="get_particular_question"),

    path('room/add_user_answer', add_user_answer, name="add_user_answer"),
    path('room/check_team_lead/<int:event_id>/<str:user_email>',
         check_team_lead, name="check_team_lead"),
    path('room/start', start_room, name="start_room"),
    path('room/is_penalty', is_penalty, name="is_penalty"),
    path('room/get_result/<str:user_email>/<int:room_id>',
         get_result, name="get result"),
    path('collection/result/<int:collection_id>/<str:user_email>',
         user_result, name="user_result"),
    path('collection/start/<int:event_id>/<str:user_email>',
         start_collection, name="start_collection"),
    path('collection/timer/<int:event_id>/<str:user_email>',
         get_timer_collection, name="get_timer_collection")

]
