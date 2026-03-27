from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    reg_no = serializers.CharField(required=True) 

    # Student specific fields (Write only)
    ttset = serializers.CharField(write_only=True)
    sem = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'reg_no', 'ttset', 'sem'
        ]

    def create(self, validated_data):
        # 1. Pop out ONLY the academic data
        student_data = {
            'ttset': validated_data.pop('ttset'),
            'sem': validated_data.pop('sem'),
        }
        
        # 2. Create the Auth User
        user = User.objects.create_user(**validated_data)
        
        # 3. Explicitly create the Student Profile linked to this new user
        from details.models import Student 
        Student.objects.create(user=user, **student_data)
        
        return user