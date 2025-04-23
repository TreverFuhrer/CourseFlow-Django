from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Course, Enrollment, adminEmail, OverrideRequest
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .adminEmails import EmailMessage
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Admin Signin
        if request.user.is_staff:
            return redirect('admin-home')
        # Advisor signin
        if request.user.groups.filter(name='Advisor').exists():
            return redirect('advisor_list')
        # Student Signin
        return redirect('student-dashboard')

    form = AuthenticationForm(request)
    return render(request, 'home.html', {'form': form})

@login_required
def student_dashboard(request):
    #TODO implemnt this
    return render(request, 'student_home.html')

@login_required
def admin_home(request):
    if not request.user.is_staff:
        return redirect('home')

    courses   = Course.objects.all()
    overrides = OverrideRequest.objects.filter(status='pending')
    students  = User.objects.filter(is_staff=False)

    return render(request, 'admin_home.html', {
        'courses':   courses,
        'overrides': overrides,
        'students':  students,
    })

#TODO implement this
@login_required
def course_create(request):
    if not request.user.is_staff:
        return redirect('home')

#TODO implement this
@login_required
def course_update(request, pk):
    if not request.user.is_staff:
        return redirect('home')

#TODO implement this
@login_required
def course_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')

#TODO implement this
@login_required
def override_action(request, pk):
    if not request.user.is_staff:
        return redirect('home')

#TODO  implemnt this
@login_required
def student_detail(request, pk):
    if not request.user.is_staff:
        return redirect('home')

@login_required
def report(request):
    if not request.user.is_staff:
        return redirect('home')

    courseCount = Course.objects.count()
    enrollment = Enrollment.objects.count()
    status = Enrollment.objects.values('status').annotate(count=Count('id'))
    return render(request, 'report.html', {
        'courseCount': courseCount,
        'enrollment': enrollment,
        'status': status,
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