from django.db import models
from django.conf import settings
import os

class LearningMaterial(models.Model):
    CATEGORY_CHOICES = (
        ('textbook', 'Textbook'),
        ('notes', 'Notes'),
        ('assignment', 'Assignment'),
        ('storybook', 'Storybook'),
        ('worksheet', 'Worksheet'),
        ('revision', 'Revision Paper'),
    )
    
    title = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, help_text="Maths, English, Science")
    target_class = models.CharField(max_length=20, help_text="e.g. Grade 5")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='materials/%Y/%m/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.target_class})"

class AccessLog(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(LearningMaterial, on_delete=models.CASCADE, related_name='access_logs')
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} accessed {self.material}"
