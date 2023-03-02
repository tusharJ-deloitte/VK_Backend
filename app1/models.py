from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.IntegerField(null=True, blank=True)
    designation = models.TextField(max_length=30, null=True, blank=True)
    profile_pic = models.TextField(null=True, blank=True)
    doj = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=200)
    author = models.TextField(max_length=20)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.TextField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField(max_length=20)
    team_size = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    activity_logo = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    activity = models.ManyToManyField(Activity, null=True)
    name = models.TextField(max_length=20, unique=True)
    current_size = models.IntegerField(default=0)
    team_lead = models.TextField(max_length=20, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    team_logo = models.TextField(blank=True, null=True)
    team_score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    activity_mode = models.TextField(max_length=20, default='online')
    event_type = models.TextField(max_length=20, default='Group')
    name = models.TextField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    min_members = models.IntegerField(default=0)
    max_members = models.IntegerField(default=0)
    cur_participation = models.IntegerField(default=0)

    # setting up choices for status
    YET_TO_START = "Yet To Start"
    ACTIVE = "Active"
    ELAPSED = "Elapsed"
    STATUS_CHOICES = [
        # (ACTUAL VALUE , HUMAN READABLE FORMAT)
        (YET_TO_START, "yet to start"),
        (ACTIVE, "active"),
        (ELAPSED, "elapsed"),
    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=YET_TO_START)

    def __str__(self) -> str:
        return self.name


class Registration(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.event.name


class Player(models.Model):
    team = models.ManyToManyField(Team)
    activity_id = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name


class IndRegistration(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.event.name


class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default="1")
    uploaded_on = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    is_uploaded = models.BooleanField(default=False)
    file_name = models.TextField(null=True, blank=True)
    file_size = models.IntegerField(default=0, null=True, blank=True)
    file_duration = models.TextField(null=True, blank=True)  # in seconds
    score = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.email


class Pod(models.Model):
    pod_id = models.IntegerField(default=0)
    pod_name = models.TextField(null=True, blank=True)
    pod_size = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.pod_name

class Quiz(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, default="1")
    banner_image = models.TextField(null=True, blank=True)
    title = models.TextField(unique=True,null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question_text = models.TextField(null=True, blank=True)
    image_clue = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    MCQ = "MCQ"
    CHECKBOX = "Checkbox"
    QUESTION_CHOICES = [
        # (ACTUAL VALUE , HUMAN READABLE FORMAT)
        (MCQ, "MCQ"),
        (CHECKBOX, "checkbox")
    ]

    question_type = models.CharField(
        max_length=20, choices=QUESTION_CHOICES, default=MCQ)
    
    max_timer = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.question_text
    

class Option(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,default=1)
    question = models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.option_text
    

class UserAnswer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    submitted_answer = models.TextField()
    is_correct_answer = models.BooleanField(null=True,blank=True,default=False)
    time_taken = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.email+" "+self.quiz.title+" "+self.question.question_text
    
   