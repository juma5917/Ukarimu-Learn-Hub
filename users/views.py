from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Count
from .models import User
from library.models import LearningMaterial, AccessLog
from .forms import UserCreateForm, UserEditForm

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'is_student': user.role == 'student',
    }
    return render(request, 'users/dashboard.html', context)

def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all().order_by('-date_joined')
    materials = LearningMaterial.objects.all().order_by('-created_at')
    
    # Analytics & Impact Stats
    total_views = AccessLog.objects.count()
    # Get top 5 most accessed materials
    popular_books = LearningMaterial.objects.annotate(
        views=Count('access_logs')
    ).order_by('-views')[:5]
    
    context = {
        'users': users,
        'materials': materials,
        'student_count': User.objects.filter(role='student').count(),
        'material_count': LearningMaterial.objects.count(),
        'total_views': total_views,
        'popular_books': popular_books,
    }
    return render(request, 'users/admin_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher' and not request.user.is_superuser:
        return redirect('dashboard')
    
    materials = LearningMaterial.objects.filter(uploaded_by=request.user).order_by('-created_at')
    return render(request, 'users/teacher_dashboard.html', {'materials': materials})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserCreateForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Add New User'})

@login_required
@user_passes_test(is_admin)
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user_obj)
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Edit User'})

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_obj.delete()
        return redirect('admin_dashboard')
    return render(request, 'users/user_confirm_delete.html', {'object': user_obj})

@login_required
@user_passes_test(is_admin)
def donor_report(request):
    # Aggregated stats
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_materials = LearningMaterial.objects.count()
    total_views = AccessLog.objects.count()
    
    # Active students (accessed content in last 30 days)
    last_30_days = timezone.now() - timezone.timedelta(days=30)
    active_students = AccessLog.objects.filter(accessed_at__gte=last_30_days).values('student').distinct().count()
    
    # Subject breakdown
    subjects = LearningMaterial.objects.values('subject').annotate(count=Count('id')).order_by('-count')
    
    # Top Content
    popular_books = LearningMaterial.objects.annotate(
        views=Count('access_logs')
    ).order_by('-views')[:10]

    context = {
        'generated_at': timezone.now(),
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_materials': total_materials,
        'total_views': total_views,
        'active_students': active_students,
        'subjects': subjects,
        'popular_books': popular_books,
    }
    return render(request, 'users/donor_report.html', context)
