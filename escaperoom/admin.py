from django.contrib import admin
from .models import Detail,Question

# Register your models here.
@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'theme', 'bg_image', 'number_of_questions', 'level']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','escape_room_id', 'images', 'options', 'context', 'number_of_images', 'question_type', 'question', 'answers', 'hints']