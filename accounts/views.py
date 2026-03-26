from rest_framework import generics, permissions
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer