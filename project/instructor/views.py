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
