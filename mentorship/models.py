from django.db import models
from django.conf import settings

class MentorshipContent(models.Model):
    CONTENT_TYPES = (
        ('video', 'Mentorship Video'),
        ('career_talk', 'Career Talk'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='mentorship/%Y/%m/', blank=True, null=True, help_text="Upload video or document")
    link = models.URLField(blank=True, null=True, help_text="Or provide a link (e.g. YouTube)")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title