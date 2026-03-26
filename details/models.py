from django.db import models
from django.contrib import admin
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ttset=models.SmallIntegerField(default=0)
    phone=models.CharField(max_length=13, blank=True, null=True)

    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
