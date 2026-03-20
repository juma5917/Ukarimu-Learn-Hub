from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    class_level = models.CharField(max_length=20, blank=True, null=True, help_text="For Students: e.g., Grade 4")

    def __str__(self):
        return f"{self.username} ({self.role})"
