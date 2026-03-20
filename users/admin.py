from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'class_level', 'is_staff']
    list_filter = ('role', 'class_level', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Ukarimu Profile Info', {'fields': ('role', 'class_level')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Ukarimu Profile Info', {'fields': ('role', 'class_level')}),
    )

admin.site.register(User, CustomUserAdmin)
