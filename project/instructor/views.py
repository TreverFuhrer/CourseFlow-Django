from django.shortcuts import render, get_object_or_404, redirect
from project.administration.models import Course, Enrollment, OverrideRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InstructorProfile

@login_required
def instructor_dashboard(request):
    instructor_profile = get_object_or_404(InstructorProfile, user=request.user)
    courses = instructor_profile.courses.all()
    return render(request, 'instructor/dashboard.html', {'courses': courses})

@login_required
def manage_enrollments(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    enrollments = course.enrollments.all()
    return render(request, 'instructor/manage_enrollments.html', {'course': course, 'enrollments': enrollments})

@login_required
def approve_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, course__instructor=request.user)
    enrollment.status = 'approved'
    enrollment.save()
    messages.success(request, 'Enrollment approved.')
    return redirect('instructor:manage_enrollments', course_id=enrollment.course.id)

@login_required
def reject_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, course__instructor=request.user)
    enrollment.status = 'rejected'
    enrollment.save()
    messages.success(request, 'Enrollment rejected.')
    return redirect('instructor:manage_enrollments', course_id=enrollment.course.id)

