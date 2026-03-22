from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LearningMaterial, AccessLog
from .forms import MaterialUploadForm
from django.db.models import Q, Count, Max
from users.models import User

@login_required
def library_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    materials = LearningMaterial.objects.all().order_by('-created_at')
    
    if category:
        materials = materials.filter(category=category)
    
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | 
            Q(subject__icontains=query) |
            Q(target_class__icontains=query)
        )
    
    return render(request, 'library/library_list.html', {'materials': materials})

@login_required
def track_access(request, pk):
    material = get_object_or_404(LearningMaterial, pk=pk)
    AccessLog.objects.create(student=request.user, material=material)
    return render(request, 'library/view_material.html', {'material': material})

@login_required
def upload_material(request):
    if request.user.role == 'student' and not (request.user.is_superuser or request.user.is_staff):
        return redirect('library_list')

    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            if request.user.role == 'admin' or request.user.is_superuser:
                return redirect('admin_dashboard')
            if request.user.role == 'teacher':
                return redirect('teacher_dashboard')
            return redirect('library_list')
    else:
        initial_data = {}
        if request.GET.get('category'):
            initial_data['category'] = request.GET.get('category')
        form = MaterialUploadForm(initial=initial_data)
    
    return render(request, 'library/upload.html', {'form': form})

def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

@login_required
def material_edit(request, pk):
    material = get_object_or_404(LearningMaterial, pk=pk)
    
    # Permissions: Admin or Owner
    if not (request.user.is_superuser or request.user.role == 'admin' or material.uploaded_by == request.user):
        return redirect('library_list')

    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            if request.user.role == 'admin' or request.user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('teacher_dashboard')
    else:
        form = MaterialUploadForm(instance=material)
    return render(request, 'library/upload.html', {'form': form, 'title': 'Edit Material'})

@login_required
def material_delete(request, pk):
    material = get_object_or_404(LearningMaterial, pk=pk)
    
    # Permissions: Admin or Owner
    if not (request.user.is_superuser or request.user.role == 'admin' or material.uploaded_by == request.user):
        return redirect('library_list')

    if request.method == 'POST':
        material.delete()
        if request.user.role == 'admin' or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('teacher_dashboard')
    
    # Determine cancel link
    cancel_url = 'teacher_dashboard' if request.user.role == 'teacher' else 'admin_dashboard'
    return render(request, 'library/material_confirm_delete.html', {'object': material, 'cancel_url': cancel_url})

@login_required
def student_reading_history(request):
    logs = AccessLog.objects.filter(student=request.user).select_related('material').order_by('-accessed_at')
    return render(request, 'library/reading_history.html', {'logs': logs})

@login_required
def teacher_monitoring(request):
    if request.user.role == 'student':
        return redirect('dashboard')
    
    student_activity = User.objects.filter(role='student').annotate(
        read_count=Count('accesslog'),
        last_active=Max('accesslog__accessed_at')
    ).order_by('-read_count')
    
    return render(request, 'library/monitoring.html', {'student_activity': student_activity})
