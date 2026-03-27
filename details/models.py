from time import timezone
from django.conf import settings

from django.db import models

class Subjects(models.Model):
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=5, unique=True)
    ttset = models.CharField(max_length=10) 
    sem = models.SmallIntegerField()
    # Deleted: year

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    ttset = models.CharField(max_length=10)
    sem = models.SmallIntegerField()
    is_available = models.BooleanField(default=False)
    # Deleted: year

class StudyMeeting(models.Model):
    topic = models.CharField(max_length=200)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, to_field='subject_code')
    creator = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='created_meetings')
    
    # Timing Logic
    created_at = models.DateTimeField(auto_now_add=True)
    meeting_time = models.DateTimeField()
    available_up_to = models.DateTimeField(help_text="Deadline to join this session")
    
    location = models.CharField(max_length=255, default="Library")
    participants = models.ManyToManyField('Student', related_name='joined_meetings', blank=True)

    @property
    def is_active(self):
        """Checks if the joining deadline has passed."""
        return timezone.now() < self.available_up_to

    def __str__(self):
        return f"{self.topic} ({self.subject.subject_code})"