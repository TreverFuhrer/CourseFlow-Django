from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student-dashboard'),
    path('enroll/', views.student_enroll_course, name='student-enroll'),
    path('override/', views.student_request_override, name='student-override-request'),
]