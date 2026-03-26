from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, StudyMeeting, Subjects
from .serializers import StudentSerializer, StudyMeetingSerializer, SubjectsSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Student, StudyMeeting
from .serializers import StudyMeetingSerializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student, StudyMeeting, Subjects
from .serializers import StudentSerializer, StudyMeetingSerializer, SubjectsSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'reg_no'

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Endpoint: GET /students/me/
        Returns the profile of the currently logged-in student.
        """
        try:
            # Get the student profile linked to the authenticated User
            student = request.user.student_profile
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student profile not found for this user."}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_me(self, request):
        """
        Endpoint: PATCH /students/me/
        Allows the student to update their own profile (like is_available).
        """
        student = request.user.student_profile
        serializer = self.get_serializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectsViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectsSerializer

    def get_queryset(self):
        return Subjects.objects.all()
    

class StudyMeetingViewSet(viewsets.ModelViewSet):
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
    # Only logged-in users can interact with meetings
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Get the student profile of the logged-in user
        student = self.request.user.student_profile
        
        # 2. Save the meeting with this student as creator
        serializer.save(creator=student)
        
        # 3. Toggle availability
        student.is_available = True
        student.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        student = request.user.student_profile

        # Only the actual creator can delete
        if instance.creator == student:
            student.is_available = False
            student.save()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    
    @action(detail=False, methods=['get'], url_path='find-available-partners')
    def find_available_partners(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "Missing subject_id"}, status=400)

        me = request.user.student_profile
        
        # Matches subject, same year/set, and currently available
        available_meetings = StudyMeeting.objects.filter(
            subject_id=subject_id,
            creator__year=me.year,
            creator__ttset=me.ttset,
            creator__is_available=True
        ).exclude(creator=me)

        serializer = self.get_serializer(available_meetings, many=True)
        return Response(serializer.data)