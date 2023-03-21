from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.registerUser, name='registerUser'),
    path('is_admin/<str:user_email>', views.is_admin, name='is_admin'),
    # category
    path('get_category/<int:pk>', views.get_category, name='get_category'),
    path('create_category', views.create_category, name='create_category'),
    path('update_category/<int:pk>', views.update_category, name="update_category"),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category'),

    # Activity
    path('create_activity', views.create_activity, name="create_activity"),
    path('update_activity/<int:pk>', views.update_activity, name="update_activity"),
    path('get_activity/<int:pk>', views.get_activity, name="get_activity"),
    path('delete_activity/<int:pk>', views.delete_activity, name="delete_activity"),
    path('get_activity_list', views.get_activity_list,
         name="get_activity_list"),

    # Teams
    path('create_teams', views.create_teams, name="create_teams"),
    path('update_teams/<int:team_id>', views.update_teams, name="update_teams"),
    path('delete_teams/<int:team_id>', views.delete_teams, name="delete_teams"),
    path('manage_teams/<str:user_email>',
         views.manage_teams, name='manage_teams'),

    # Events
    path('create_event', views.create_event, name='create_event'),
    path('get_all_events', views.get_all_events, name='get_all_events'),
    path('update_event/<int:event_id>', views.update_event, name='update_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),

    # Event Registration
    path('event/register', views.register, name='register'),
    path('event/get_all_registrations/<int:event_id>',
         views.get_all_registrations, name='get_all_registrations'),
    path('event/update_score', views.update_score, name="update_score"),
    path('event/register/ind', views.register_individual, name='register'),
    path('event/register/cancel/<int:event_id>/<p_id>',
         views.cancel_registration, name="cancel_registration"),

    # leaderboard-overall
    path('get_rank_by_activity/<int:activity_id>', views.get_rank_by_activity,
         name="get_rank_by_ctivity"),
    path('get_overall_rank', views.get_overall_rank,
         name="get_overall_rank"),

    # wall of fame
    path('hottest_challenge', views.get_hottest_challenge,
         name="hottest_challenge"),
    path('top_performer', views.get_top_performer, name='top_performer'),
    path('star_of_week', views.get_star_of_week, name='star_of_week'),

    # personal stats
    path('events_participated/<str:user_email>', views.get_events_participated,
         name='events_participated'),
    path('my_rank/<str:user_email>', views.get_my_rank,
         name='my_rank'),


    # leaderboard-personal
    path('my_top_events/<str:user_email>', views.get_top_events_participated,
         name='my_top_events'),
    path('get_my_score/<str:user_email>', views.get_my_score,
         name='get_my_score'),
    path('get_top_events_activity/<str:user_email>/<int:activity_id>', views.get_top_events_by_activity,
         name='get_top_events_activity'),



    # plank
    path('upload_aws', views.upload_aws, name="upload_aws"),
    path('upload/<str:user_email>/<str:event_name>',views.upload,name="upload"),
    # path('edit_upload/<str:user_email>',views.edit_upload,name="edit_upload"),
#     path('get_files_list', views.get_files_list, name="get_files_list"),
    path('get_list_user_event/<str:user_email>/<str:event_name>',views.get_list_user_event,name="get_list_user_event"),
    path('get_uploads/<str:event_name>',views.get_uploads,name="get_uploads"),
    path('get_uploads_by_date/<str:event_name>/<str:date>',views.get_uploads_by_date,name="get_uploads_by_date"),
    path('delete_file/<int:upload_id>',views.delete_file,name="delete_file"),


    # integration PODS & DNA
    path("get_pods/<str:user_email>", views.get_pods, name='get_pods_data'),
    path("get_users_dna", views.get_all_user_dna, name='get_all_user_dna'),
    path("get_users_org", views.get_all_users_organisation,
         name='get_all_users_organisation'),

    # sns test
    path("sns", views.sns, name="sns"),

    #tech quiz apis
    path("quiz/create",views.create_quiz,name="create_quiz"), 
    path("quiz/get_library", views.get_library_for_quizs,name="get_library_for_quizs"),
    path("quiz/get_quiz_info/<int:quizId>",views.get_quiz_information, name="get_quiz_information"),
    path("quiz/add_user_answer",views.add_user_answer,name="add_user_answer"),
    path("quiz/score_summary",views.score_summary,name="score_summary"),
    path("quiz/create_quizquestion", views.create_quizquestion,name="create_quizquestion"),
    path("quiz/publish", views.publish_quiz_for_event,name="publish_quiz_for_event"),
    path("quiz/edit",views.edit_quiz,name="edit_quiz"),
    path("quiz/delete/<int:quiz_id>",views.delete_quiz,name="delete_quiz"),
    path("quiz/add_new_question",views.add_new_question,name="add_new_question"),
    path("quiz/delete_quiz_question/<int:quiz_id>/<int:question_number>",views.delete_quiz_question,name="delete_quiz_question"),
    path("quiz/edit_quiz_question",views.edit_quiz_question,name="edit_quiz_question"),
    path("quiz/get_question/<int:quiz_id>/<int:question_number>",views.get_particular_question,name="get_particular_question")


    path("notifications/<str:user_email>", views.get_notifications_of_user, name="get_notifications_of_user")

]
