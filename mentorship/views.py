from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MentorshipContent, Announcement
from .forms import MentorshipContentForm, AnnouncementForm

@login_required
def mentorship_list(request):
    contents = MentorshipContent.objects.all().order_by('-created_at')
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'mentorship/list.html', {
        'contents': contents,
        'announcements': announcements,
        'is_mentor': request.user.role in ['mentor', 'admin'] or request.user.is_superuser
    })

@login_required
def upload_content(request):
    if request.user.role not in ['mentor', 'admin'] and not request.user.is_superuser:
        return redirect('mentorship_list')
    
    if request.method == 'POST':
        form = MentorshipContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.uploaded_by = request.user
            content.save()
            return redirect('mentorship_list')
    else:
        form = MentorshipContentForm()
    return render(request, 'mentorship/upload_content.html', {'form': form})

@login_required
def post_announcement(request):
    if request.user.role not in ['mentor', 'admin'] and not request.user.is_superuser:
        return redirect('mentorship_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.posted_by = request.user
            announcement.save()
            return redirect('mentorship_list')
    else:
        form = AnnouncementForm()
    return render(request, 'mentorship/post_announcement.html', {'form': form})

@login_required
def delete_mentorship_content(request, pk):
    content = get_object_or_404(MentorshipContent, pk=pk)
    
    # Allow deletion if user is superuser, admin role, or the uploader
    if not (request.user.is_superuser or request.user.role == 'admin' or content.uploaded_by == request.user):
        return redirect('mentorship_list')

    if request.method == 'POST':
        content.delete()
        return redirect('mentorship_list')
    
    return render(request, 'mentorship/confirm_delete.html', {'object': content})