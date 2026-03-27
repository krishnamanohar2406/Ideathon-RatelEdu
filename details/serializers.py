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
    
    # ADD THESE TWO LINES to pull the names from the User model
    reg_no = serializers.ReadOnlyField(source='user.reg_no')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = Student
        fields = [
            'id','reg_no', 'first_name', 'last_name', 'username', 
            'email', 'ttset', 'sem', 'is_available'
        ]

class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['username', 'name']

    def get_name(self, obj):
        # Combines first and last name cleanly
        return f"{obj.first_name} {obj.last_name}".strip()

# ... (Keep your StudentSerializer and SubjectsSerializer as they are) ...

# 2. Update StudyMeetingSerializer to use it
class StudyMeetingSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField(source='creator.first_name')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    is_open = serializers.ReadOnlyField(source='is_active')
    
    # 3. Apply the Participant format here
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = StudyMeeting
        fields = [
            'id', 'topic', 'subject', 'subject_name', 'creator_name', 
            'created_at', 'meeting_time', 'available_up_to', 
            'location', 'is_open', 'participants'
        ]
        read_only_fields = ['created_at', 'creator_name']