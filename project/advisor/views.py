from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from administration.models import Course, Enrollment
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def advisor_home(request):
    if not request.user.groups.filter(name='Advisor').exists():
        return redirect('home')

    courses = Course.objects.all()
    students = User.objects.filter(groups__name='Student').order_by('username')

    return render(request, 'advisor/advisor.html', {
        'courses':   courses,
        'students':  students,
    })

@login_required
def send_message(request, recipient_id):
    if request.method == 'POST':
        recipient = User.objects.get(pk=recipient_id)
        Message.objects.create(sender=request.user, recipient=recipient, content=request.POST['content'])
    return redirect('view_conversation', recipient_id=recipient_id)

@login_required
def view_conversation(request, recipient_id):
    recipient = User.objects.get(pk=recipient_id)
    messages = Message.objects.filter(
        Q(sender=request.user,   recipient=recipient) |
        Q(sender=recipient,      recipient=request.user)
    ).order_by('timestamp')
    return render(request, 'chat/conversation.html', {
        'recipient': recipient,
        'messages': messages,
    })

@login_required
def advisor_list(request):
    students = User.objects.filter(groups__name='Student').order_by('username')
    return render(request, 'advisor/advisor_list.html', {'students': students})

@login_required
def advisor_detail(request, pk):
    if not request.user.groups.filter(name='Advisor').exists():
        return redirect('home')

    student = get_object_or_404(User, pk=pk, groups__name='Student')
    enrollments = student.enrollments.all()

    taken_courses = set(e.course for e in enrollments if e.status == 'approved')
    all_courses = set(Course.objects.all())
    available_courses = all_courses - taken_courses
    recommended_courses = []
    for c in available_courses:
        prereqs = set(c.prerequisites.all())
        if prereqs <= taken_courses:
            recommended_courses.append(c)

    return render(request, 'advisor/studentinfo.html', {
        'student': student,
        'enrollments': enrollments,
        'recommended_courses': recommended_courses,
    })

@login_required
def enrollment_action(request, enr_id):
    if not request.user.groups.filter(name='Advisor').exists():
        return redirect('home')

    enroll = get_object_or_404(Enrollment, pk=enr_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            enroll.status = 'approved'
        elif action == 'reject':
            enroll.status = 'rejected'
        enroll.save()
    return redirect('advisor-student-detail', pk=enroll.student.pk)