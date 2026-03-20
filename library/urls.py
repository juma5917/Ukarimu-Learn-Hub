from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.library_list, name='library_list'),
    path('history/', views.student_reading_history, name='reading_history'),
    path('monitoring/', views.teacher_monitoring, name='reading_monitoring'),
    path('upload/', views.upload_material, name='upload_material'),
    path('material/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('material/<int:pk>/delete/', views.material_delete, name='material_delete'),
    path('material/<int:pk>/access/', views.track_access, name='track_access'),
]