from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Course, Enrollment, adminEmail
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .adminEmails import EmailMessage

# Create your views here.
def home(request):
    return render(request, 'home.html')

def report(request):
    courseCount = Course.objects.count()
    enrollment = Enrollment.objects.count()
    status = Enrollment.objects.values('status').annotate(count=Count('id'))

    context = {
        'courseCount': courseCount,
        'enrollment': enrollment,
        'status': status,
    }
    return render(request, 'report.html', context)

def email(request):
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