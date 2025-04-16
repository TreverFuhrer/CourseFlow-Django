from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Course, Enrollment

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