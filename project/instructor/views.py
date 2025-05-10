# instructor/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from administration.models import Course, Enrollment, OverrideRequest
from django.http import HttpResponseForbidden

@login_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructor/dashboard.html', {'courses': courses})

@login_required
def manage_enrollments(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    enrollments = course.enrollments.all()
    return render(request, 'instructor/manage_enrollments.html', {'course': course, 'enrollments': enrollments})

@login_required
def approve_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        return HttpResponseForbidden("You do not have permission to approve this enrollment.")
    enrollment.status = 'approved'
    enrollment.save()
    messages.success(request, 'Enrollment approved.')
    return redirect('instructor:instructor-manage-enrollments', course_id=enrollment.course.id)

@login_required
def reject_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        return HttpResponseForbidden("You do not have permission to reject this enrollment.")
    enrollment.status = 'rejected'
    enrollment.save()
    messages.success(request, 'Enrollment rejected.')
    return redirect('instructor:instructor-manage-enrollments', course_id=enrollment.course.id)

@login_required
def update_course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.seat_limit = request.POST.get('seat_limit')
        course.save()
        messages.success(request, 'Course details updated.')
        return redirect('instructor:instructor-dashboard')
    return render(request, 'instructor/update_course.html', {'course': course})