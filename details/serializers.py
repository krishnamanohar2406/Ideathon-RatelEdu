from rest_framework import serializers
from .models import Student, Subjects, StudyMeeting

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    # Pull data from the linked User model
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Student
        fields = [
            'reg_no', 'first_name', 'last_name', 'username', 
            'email', 'year', 'ttset', 'sem', 'is_available'
        ]

class StudyMeetingSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField(source='creator.first_name')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    participant_count = serializers.IntegerField(source='participants.count', read_only=True)

    class Meta:
        model = StudyMeeting
        fields = ['id', 'topic', 'subject', 'subject_name', 'creator', 'creator_name', 'meeting_time', 'location', 'participant_count', 'participants']