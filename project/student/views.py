from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from administration.models import Course, Enrollment, OverrideRequest

@login_required
def student_dashboard(request):
    student = request.user
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'student/student_dashboard.html', {'enrollments': enrollments})

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


@login_required
def student_course_search(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(Q(title__icontains=query) | Q(instructor__username__icontains=query)) if query else []

    return render(request, 'student/course_search_results.html', {'courses': courses, 'query': query})


@login_required
def student_all_courses(request):
    courses = Course.objects.all()
    return render(request, 'student/all_courses.html', {'courses': courses})

@login_required
def student_course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render(request, 'student/course_detail.html', {'course': course})


@login_required
def drop_course(request, enrollment_id):
    if not request.user.is_authenticated:
        return redirect ('login')

    try:
        enrollment = Enrollment.objects.get(pk=enrollment_id, student=request.user)
        enrollment.delete()
    except Enrollment.DoesNotExist:
        pass
    return redirect ('student-dashboard')



@login_required
def join_waitlist(request, course_id):
    if not request.user.is_authenticated:
        return redirect ('login')

    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':

        OverrideRequest.objects.create(course=course, student=request.user, reason='waitlist request', status='waitlist')
        return redirect ('student-dashboard')

    return render(request, 'student/join_waitlist.html', {'course': course})