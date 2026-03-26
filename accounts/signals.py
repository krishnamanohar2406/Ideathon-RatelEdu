from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from details.models import Student

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        # We create a "blank" student profile linked to the new User.
        # Note: You'll need to update these fields later via the /students/me/ PATCH endpoint
        # because the User registration doesn't include year/ttset yet.
        Student.objects.create(
            user=instance,
            reg_no=f"TEMP_{instance.id}", # Temporary reg_no until updated
            first_name=instance.first_name or instance.username,
            last_name=instance.last_name or "",
            year=1,      # Default starting year
            ttset="A",   # Default set
            sem=1        # Default semester
        )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_student_profile(sender, instance, **kwargs):
    # This ensures that if the User object is saved, the Student object is also saved
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()