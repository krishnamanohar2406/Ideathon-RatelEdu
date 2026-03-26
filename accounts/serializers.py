# from djoser.serializers import UserSerializer as BaseUserSerializer , UserCreateSerializer as BaseUserCreateSerializer

# class UserCreateSerializer (BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields =[ 'id', 'username', 'email', 'first_name', 'last_name', 'password']


# class UserSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']


# from django.contrib.auth.models import User

# from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Hash the password during creation
        user = User.objects.create_user(**validated_data)
        return user