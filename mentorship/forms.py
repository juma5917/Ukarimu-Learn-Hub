from django import forms
from .models import MentorshipContent, Announcement

class MentorshipContentForm(forms.ModelForm):
    class Meta:
        model = MentorshipContent
        fields = ['title', 'content_type', 'description', 'file', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }