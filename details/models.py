from django.db import models

class Subjects(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    ttset = models.CharField(max_length=10) 
    sem = models.SmallIntegerField()

    def __str__(self):
        return f"{self.name} ({self.ttset})"

from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Student(models.Model):
    # Link to the User account
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    
    # We use reg_no as the primary key as you requested
    reg_no = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Academic Data
    year = models.IntegerField()
    ttset = models.CharField(max_length=10)
    sem = models.SmallIntegerField()
    
    # Matching Logic
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reg_no} ({self.user.username})"

class StudyMeeting(models.Model):
    topic = models.CharField(max_length=200)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    creator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='created_meetings')
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=255, default="Library / Online")
    
    # Many students can join one meeting
    participants = models.ManyToManyField(Student, related_name='joined_meetings', blank=True)

    def __str__(self):
        return f"{self.topic} - {self.subject.name}"