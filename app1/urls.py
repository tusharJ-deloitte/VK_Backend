from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('is_admin/<int:userId>', views.is_admin, name='is_admin'),
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
    path('get_activity_list', views.get_activity_list, name="get_activity_list"),

    # Teams
    path('create_teams', views.create_teams, name="create_teams"),
    path('update_teams/<int:team_id>', views.update_teams, name="update_teams"),
    path('delete_teams/<int:team_id>', views.delete_teams, name="delete_teams"),
    path('manage_teams/<int:user_id>', views.manage_teams, name='manage_teams'),

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

    # leaderboard
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

    path('events_participated/<int:user_id>', views.get_events_participated,
         name='events_participated'),
    path('my_rank/<int:user_id>', views.get_my_rank,
         name='my_rank'),

     #integration PODS & DNA
     path("get_pods",views.get_pods_data,name='get_pods_data'),
     path("get_users_dna",views.get_all_user_dna,name='get_pods_data'),

]
