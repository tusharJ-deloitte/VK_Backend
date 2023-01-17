from django.contrib import admin
from .models import Post, Category, Activity, Team, Player, Upload

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team_size', 'created_on', 'category_id','activity_logo']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on','team_lead','current_size','team_logo']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'score','user_id']

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','uploaded_file']
