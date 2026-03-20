from django.contrib import admin
from .models import LearningMaterial

@admin.register(LearningMaterial)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'target_class', 'category', 'uploaded_by', 'created_at')
    list_filter = ('target_class', 'subject', 'category')
    search_fields = ('title', 'subject', 'description')
    date_hierarchy = 'created_at'
