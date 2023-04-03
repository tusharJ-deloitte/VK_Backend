from django.contrib import admin
from .models import MysteryRoomCollection, MysteryRoom, MysteryRoomOption, MysteryRoomQuestion, MRUserAnswer


@admin.register(MysteryRoomCollection)
class MysteryRoomCollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_id', 'banner_image', 'title', 'number_of_team_members',
                    'number_of_mystery_rooms', 'theme', 'created_on', 'last_modified']


@admin.register(MysteryRoom)
class MysteryRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'mystery_room', 'banner_image', 'title', 'difficulty_level',
                    'number_of_questions', 'description', 'created_on', 'last_modified']


@admin.register(MysteryRoomQuestion)
class MysteryRoomQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'mystery_room_collection', 'question_number', 'question_text',
                    'question_image', 'note', 'hint_text', 'hint_image', 'question_type', 'created_on', 'last_modified']


@admin.register(MysteryRoomOption)
class MysteryRoomOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'question', 'option_text',
                    'is_correct', 'created_on', 'last_modified']


@admin.register(MRUserAnswer)
class MRUserAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_id', 'mr_collection', 'mr_room',
                    'mr_question', 'submitted_answer', 'is_correct', 'time_taken', 'score']
