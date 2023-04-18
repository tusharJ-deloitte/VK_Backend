from django.db import models
from datetime import datetime
import pytz


class MysteryRoomCollection(models.Model):
    event_id = models.IntegerField(default=0)
    banner_image = models.TextField(null=True, blank=True)
    title = models.TextField(unique=True, null=True, blank=True)
    number_of_mystery_rooms = models.IntegerField(default=0)
    theme = models.TextField(null=True, blank=True)
    created_on = models.TextField(null=True, blank=True)
    last_modified = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class MysteryRoom(models.Model):
    mystery_room = models.ForeignKey(
        MysteryRoomCollection, on_delete=models.CASCADE)
    room_number = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=True)
    banner_image = models.TextField(null=True, blank=True)
    title = models.TextField(unique=True, null=True, blank=True)
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    DIFFICULTY = [(EASY, "EASY"), (MEDIUM, "MEDIUM"), (HARD, "HARD")]
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY, default=EASY)
    number_of_questions = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.TextField(null=True, blank=True)
    last_modified = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class MysteryRoomQuestion(models.Model):
    room = models.ForeignKey(MysteryRoom, on_delete=models.CASCADE)
    mystery_room_collection = models.ForeignKey(
        MysteryRoomCollection, on_delete=models.CASCADE)
    question_number = models.IntegerField(null=True, blank=True)
    question_text = models.TextField(null=True, blank=True)
    question_image = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    hint_text = models.TextField(null=True, blank=True)
    hint_image = models.TextField(null=True, blank=True)
    MCQ = "MCQ"
    CHECKBOX = "Checkbox"
    TEXTFIELD = "TextField"
    QUESTION_CHOICES = [
        # (ACTUAL VALUE , HUMAN READABLE FORMAT)
        (MCQ, "MCQ"),
        (CHECKBOX, "Checkbox"),
        (TEXTFIELD, "TextField")
    ]
    question_type = models.CharField(
        max_length=20, choices=QUESTION_CHOICES, default=MCQ)

    def __str__(self) -> str:
        return self.question_text


class MysteryRoomOption(models.Model):
    room = models.ForeignKey(MysteryRoom, on_delete=models.CASCADE)
    question = models.ForeignKey(MysteryRoomQuestion, on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.option_text


class MRUserAnswer(models.Model):
    team_id = models.IntegerField(default=0)
    mr_collection = models.ForeignKey(
        MysteryRoomCollection, on_delete=models.CASCADE)
    mr_room = models.ForeignKey(MysteryRoom, on_delete=models.CASCADE)
    mr_question = models.ForeignKey(
        MysteryRoomQuestion, on_delete=models.CASCADE)
    submitted_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.submitted_answer


class Timer(models.Model):
    team_id = models.IntegerField(default=0)
    user_email = models.TextField(null=True, blank=True)
    room = models.ForeignKey(MysteryRoom, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    penalty = models.IntegerField(default=0)
    end_time = models.DateTimeField(null=True)
    latest_question = models.IntegerField(default=1)
    is_complete = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.team_id)
