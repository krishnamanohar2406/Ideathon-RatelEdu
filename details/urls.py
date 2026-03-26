from django.urls import path,include
from . import views
# from django 
from rest_framework.routers import SimpleRouter,DefaultRouter

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='student')
