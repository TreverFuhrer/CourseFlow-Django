from django.urls import path
from . import views

app_name = 'instructor'

urlpatterns = [
    path('dashboard/', views.instructor_dashboard, name='instructor-dashboard'),
    path('manage_enrollments/<int:course_id>/', views.manage_enrollments, name='instructor-manage-enrollments'),
    path('approve_enrollment/<int:enrollment_id>/', views.approve_enrollment, name='instructor-approve-enrollment'),
    path('reject_enrollment/<int:enrollment_id>/', views.reject_enrollment, name='instructor-reject-enrollment'),
    path('update_course/<int:course_id>/', views.update_course_details, name='instructor-update-course'),

    # Special override requests
    path('override_requests/', views.override_requests_list, name='instructor-override-requests'),
    path('override_requests/<int:req_id>/approve/', views.approve_override, name='instructor-approve-override'),
    path('override_requests/<int:req_id>/reject/', views.reject_override, name='instructor-reject-override'),

    # Email student
    path('enrollment/<int:enrollment_id>/email/', views.email_student, name='instructor-email-student'),
]