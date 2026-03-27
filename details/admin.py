from django.contrib import admin
from .models import Student, Subjects, StudyMeeting

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Fetching name and reg_no dynamically from the User model
    list_display = ('get_reg_no', 'get_first_name', 'ttset', 'is_available')
    list_filter = ( 'ttset', 'sem', 'is_available')
    
    # Searching through the linked User model
    search_fields = ('user__reg_no', 'user__username', 'user__first_name', 'user__last_name')

    fieldsets = (
        ("Account Link", {'fields': ('user',)}),
        ("Academic Details", {'fields': ( 'ttset', 'sem')}),
        ("Status", {'fields': ('is_available',)}),
    )

    # Helpers to display User data in the Student list
    def get_reg_no(self, obj):
        return obj.user.reg_no
    get_reg_no.short_description = 'Registration No'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'name', 'ttset', 'sem')
    list_filter = ( 'ttset', 'sem')
    search_fields = ('subject_code', 'name')

@admin.register(StudyMeeting)
class StudyMeetingAdmin(admin.ModelAdmin):
    list_display = ('topic', 'subject', 'creator', 'available_up_to', 'location', 'is_active')
    list_filter = ('subject', 'available_up_to')
    # Searching by the creator's reg_no inside the User model
    search_fields = ('topic', 'creator__user__reg_no', 'subject__subject_code')
    
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at',)