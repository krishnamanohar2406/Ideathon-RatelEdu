from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from details.models import Student

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Profile Details'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline, )
    
    # Added reg_no to the main list view
    list_display = ('username', 'reg_no', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'reg_no')
    
    # This tells Django to show your custom 'reg_no' field on the edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Custom User Fields', {'fields': ('reg_no',)}),
    )

    actions = ['promote_to_admin', 'demote_to_student']

    @admin.action(description="Promote selected users to Admin (Staff)")
    def promote_to_admin(self, request, queryset):
        queryset.update(is_staff=True)

    @admin.action(description="Demote selected users to regular Student")
    def demote_to_student(self, request, queryset):
        queryset.update(is_staff=False, is_superuser=False)