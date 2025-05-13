from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Course, Enrollment, adminEmail, OverrideRequest
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .adminEmails import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from django import forms

User = get_user_model()

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Admin Signin
        if request.user.is_staff:
            return redirect('admin-home')
        # Advisor signin
        if request.user.groups.filter(name='Advisor').exists():
            return redirect('advisor-home')
        # Instructor login
        if request.user.groups.filter(name='Instructor').exists():
            return redirect('instructor:instructor-dashboard')
        # Student Signin
        return redirect('student-dashboard')

    form = AuthenticationForm(request)
    return render(request, 'home.html', {'form': form})

@login_required
def student_dashboard(request):
    #TODO implemnt this
    return render(request, 'student/student_dashboard.html')


def admin_home(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')

    courses   = Course.objects.all()
    overrides = OverrideRequest.objects.filter(status='pending')
    students  = User.objects.filter(is_staff=False)

    return render(request, 'admin_home.html', {
        'courses':   courses,
        'overrides': overrides,
        'students':  students,
    })

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'seat_limit', 'prerequisites', 'instructor']


@login_required
def course_create(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
    else:
        form = CourseForm()
    return render(request, 'admin/courseform.html', {'form': form, 'action': 'Add'})

@login_required
def course_update(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    course = Course.objects.get(pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin/courseform.html', {'form': form, 'action': 'Edit'})


@login_required
def course_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    course = Course.objects.get(pk=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('admin-home')

    return render(request, 'admin/coursedelete.html', {'course': course})


@login_required
def override_action(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    override = OverrideRequest.objects.get(pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            override.status = 'approved'
        elif action == 'reject':
            override.status = 'rejected'
        override.save()
        return redirect('admin-home')

    return render(request, 'admin/overridestudent.html', {'override': override})


@login_required
def student_detail(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    student = User.objects.get(pk=pk)
    enrollments = student.enrollments.all()

    return render(request, 'admin/studentinfo.html', {
        'student': student,
        'enrollments': enrollments
    })


def report(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')

    courseCount = Course.objects.count()
    enrollment = Enrollment.objects.count()
    status = Enrollment.objects.values('status').annotate(count=Count('id'))

    popular = Course.objects.annotate(student_count=Count('enrollments')).order_by('-student_count')[:5]

    coursesfill = []
    for course in Course.objects.all():
        enrolled = course.enrollments.filter(status='approved').count()
        fill = (enrolled / course.seat_limit) * 100 if course.seat_limit > 0 else 0
        coursesfill.append({'course': course, 'enrolled': enrolled, 'seat_limit': course.seat_limit, 'fill': round(fill, 1)})

    coursesfill = sorted(coursesfill, key=lambda x: x['fill'], reverse=True)

    status_by_course = {}
    for course in Course.objects.all():
        status_counts = course.enrollments.values('status').annotate(count=Count('id'))
        status_by_course[course.title] = {item['status']: item['count'] for item in status_counts}
    
    return render(request, 'report.html', {
        'courseCount': courseCount,
        'enrollment': enrollment,
        'status': status,
        'popular_courses': popular,
        'courses_with_fill_rate': coursesfill,
        'status_by_course': status_by_course,
    })

@login_required
def email(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = EmailMessage(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            send_mail(
                email.subject,
                email.message,
                settings.DEFAULT_FROM_EMAIL,
                [email.email],
                fail_silently=False,
            )
            email.save()
            return redirect('admin-email')
    else:
        form = EmailMessage()
    sent = adminEmail.objects.all().order_by('-date')
    return render(request, 'admin/email.html', {'form': form, 'sent': sent})