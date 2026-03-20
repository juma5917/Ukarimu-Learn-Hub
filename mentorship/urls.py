from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentorship_list, name='mentorship_list'),
    path('upload/', views.upload_content, name='upload_mentorship_content'),
    path('announce/', views.post_announcement, name='post_announcement'),
    path('content/<int:pk>/delete/', views.delete_mentorship_content, name='delete_mentorship_content'),
]