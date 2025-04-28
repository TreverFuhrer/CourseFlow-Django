from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..administration.models import Course, Enrollment, OverrideRequest

@login_required
def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect ('login')

    #Show all enrollments the student is currently in
    enrollments = Enrollment.objects.filter(student=request.user)

    return render(request, 'student/dashboard.html', {'enrollments': enrollments})

@login_required
def student_enroll_course(request, course_id):
    if not request.user.is_authenticated:
        return redirect ('login')

    course = Course.objects.get(pk=course_id)

    #Check if already enrolled
    existing_enrollment = Enrollment.objects.filter(course=course, student=request.user).first()
    if existing_enrollment:
        return redirect ('student-dashboard')

    if request.method == 'POST':
        Enrollment.objects.create(course=course, student=request.user, status='enrolled')
        return redirect ('student-dashboard')

    return render(request, 'student/enroll_confirm.html', {'course': course})

@login_required
def student_request_override(request, course_id):
    if not request.user.is_authenticated:
        return redirect ('login')

    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':
        reason = request.POST.get('reason', '')

        OverrideRequest.objects.create(course=course, student=request.user, reason=reason, status='pending')
        return redirect ('student-dashboard')

    return render(request, 'student/override_request.html', {'course': course})