from django.urls import path
from .views import current_user

urlpatterns = [
    path('api/user/me/', current_user, name='current_user'),
    # path('', RegisterView.as_view(), name='register'),
]