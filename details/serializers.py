from rest_framework import serializers
from .models import Details

class StudentSerializer(serializers.ModelSerialziers):
    class Meta:
        model=Details
        feilds=['name','email','phone','ttset','']
