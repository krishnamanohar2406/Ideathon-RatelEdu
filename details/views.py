from django.utils import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, StudyMeeting, Subjects
from .serializers import StudentSerializer, StudyMeetingSerializer, SubjectsSerializer

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission: 
    - Admins (is_staff or is_superuser) can access everything.
    - Regular users can only access their own objects.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Check if the object belongs to the user
        if isinstance(obj, Student):
            return obj.user == request.user
        if isinstance(obj, StudyMeeting):
            return obj.creator.user == request.user
        return False

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    lookup_field = 'reg_no'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Student.objects.all()
        return Student.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsAdminOrOwner()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            student = request.user.student_profile
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        student = request.user.student_profile
        serializer = self.get_serializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class SubjectsViewSet(viewsets.ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer
    # Usually, anyone can view subjects, but only admins can create/delete
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class StudyMeetingViewSet(viewsets.ModelViewSet):
    serializer_class = StudyMeetingSerializer

    def get_queryset(self):
        """Only show meetings that haven't expired yet."""
        now = timezone.now() # This will now work correctly!
        queryset = StudyMeeting.objects.filter(available_up_to__gt=now)
        
        if self.request.user.is_staff:
            return queryset
        
        student = self.request.user.student_profile
        return queryset.filter(subject__sem=student.sem, subject__ttset=student.ttset)

    def perform_create(self, serializer):
        # AUTOMATION: Set creator to the logged-in student
        student = self.request.user.student_profile
        serializer.save(creator=student)
        
        # Update student availability status
        student.is_available = True
        student.save()

    @action(detail=False, methods=['get'], url_path='find-by-code')
    def find_by_code(self, request):
        """
        Endpoint: /api/meetings/find-by-code/?code=CS101
        """
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Provide a subject_code"}, status=400)

        me = request.user.student_profile
        now = timezone.now()

        # 1. Subject code match
        # 2. Same Timetable (Year/Set)
        # 3. Not expired (available_up_to > now)
        # 4. Not my own meeting
        matches = StudyMeeting.objects.filter(
            subject__subject_code=code,
            subject__year=me.year,
            subject__ttset=me.ttset,
            available_up_to__gt=now
        ).exclude(creator=me)

        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        meeting = self.get_object()
        
        # Check if the meeting is still open for joining
        if not meeting.is_active:
            return Response({"error": "This meeting is no longer open for joining."}, status=400)
            
        student = request.user.student_profile
        
        # 1. Add them to the dictionary list
        meeting.participants.add(student)
        
        # 2. Automatically make them available
        student.is_available = True
        student.save()
        
        return Response({
            "status": "Joined successfully!",
            "is_available": student.is_available
        })