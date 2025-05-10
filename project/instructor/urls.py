from django.urls import path
from . import views

app_name = 'instructor'

urlpatterns = [
    path('dashboard/', views.instructor_dashboard, name='instructor-dashboard'),
    path('manage_enrollments/<int:course_id>/', views.manage_enrollments, name='instructor-manage-enrollments'),
    path('approve_enrollment/<int:enrollment_id>/', views.approve_enrollment, name='instructor-approve-enrollment'),
    path('reject_enrollment/<int:enrollment_id>/', views.reject_enrollment, name='instructor-reject-enrollment'),
    path('update_course/<int:course_id>/', views.update_course_details, name='instructor-update-course'),
]