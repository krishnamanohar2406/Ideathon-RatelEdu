from django.urls import path,include
from . import views
# from django 
from rest_framework.routers import SimpleRouter,DefaultRouter

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='student')
router.register('subjects', views.SubjectsViewSet, basename='subjects')
router.register('meetings', views.StudyMeetingViewSet, basename='meetings')

urlpatterns = [
    path('', include(router.urls)),
]
