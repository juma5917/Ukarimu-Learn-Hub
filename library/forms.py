from django import forms
from .models import LearningMaterial

class MaterialUploadForm(forms.ModelForm):
    class Meta:
        model = LearningMaterial
        fields = ['title', 'subject', 'target_class', 'category', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }