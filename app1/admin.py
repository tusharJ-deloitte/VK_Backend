from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import   Detail, Post, Category, Activity, Team, Player, Event, Registration

class DetailInline(admin.StackedInline):
    model = Detail
    can_delete = False

class CustomizedUserAdmin(UserAdmin):
    inlines = (DetailInline,)

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team_size',
                    'created_on', 'category_id', 'activity_logo']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on',
                    'team_lead', 'current_size', 'team_score', 'team_logo']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'user_id', 'activity_id']


@admin.register(Registration)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_id', 'team_id']


@admin.register(Event)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'activity_id', 'created_on', 'activity_mode', 'start_date', 'end_date', 'start_time', 'end_time',
                    'max_teams', 'max_members', 'first_prize', 'second_prize', 'third_prize', 'cur_participation', 'status']
