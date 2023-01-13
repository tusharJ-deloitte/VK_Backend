from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_category/<int:pk>', views.get_category, name='get_category'),
    path('create_category', views.create_category, name='create_category'),
    path('update_category/<int:pk>', views.update_category, name="update_category"),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category'),
    path('create_activity', views.create_activity, name="create_activity"),
    path('update_activity/<int:pk>', views.update_activity, name="update_activity"),
    path('get_activity/<int:pk>', views.get_activity, name="get_activity"),
    path('delete_activity/<int:pk>', views.delete_activity, name="delete_activity"),
    path('create_teams', views.create_teams, name="create_teams"),
    path('update_teams/<int:team_id>', views.update_teams, name="update_teams"),
    path('delete_teams/<int:team_id>', views.delete_teams, name="delete_teams"),
    path('manage_teams/<int:user_id>', views.manage_teams, name='manage_teams'),
    path('create_event', views.create_event, name='create_event'),
    path('get_all_events', views.get_all_events, name='get_all_events'),
    path('update_event/<int:event_id>', views.update_event, name='update_event')
]
