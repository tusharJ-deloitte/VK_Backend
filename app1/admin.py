from django.contrib import admin
from .models import Post, Category, Activity, Team, Player, Event, Registration, Detail, IndRegistration, Pod, Upload,Quiz,QuizQuestion,Option,UserAnswer
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class DetailInline(admin.StackedInline):
    model = Detail
    can_delete = False


class CustomizedUserAdmin(UserAdmin):
    inlines = (DetailInline,)


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

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


@admin.register(IndRegistration)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_id', 'player_id']


@admin.register(Detail)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'employee_id',
                    'designation', 'profile_pic', 'doj']


@admin.register(Event)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'activity_id', 'created_on', 'event_type', 'activity_mode', 'start_date', 'end_date', 'start_time', 'end_time',
                    'min_members', 'max_members', 'cur_participation', 'status','task_id']


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'user', 'uploaded_on', 'is_uploaded',
                    'file_name', 'file_size', 'file_duration', 'score']


@admin.register(Pod)
class PodAdmin(admin.ModelAdmin):
    list_display = ['pod_id', 'user', 'pod_name', 'pod_size']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id','event_id','banner_image','title','number_of_questions','desc','last_modified']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['id','quiz','question_text','image_clue','note','question_type','max_timer','points','question_number']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id','quiz','question','option_text','is_correct']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display=['id','user','quiz','question','submitted_answer','is_correct_answer','time_taken','score']
