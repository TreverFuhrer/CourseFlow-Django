from django.urls import path
from . import views

urlpatterns = [
    path('student-home/', views.student_dashboard, name='student-dashboard'),
    path('search-classes/', views.student_course_search, name='student-class-search'),
    path('all classes/', views.student_all_courses, name='student-view-all-courses'),
    path('class/<int:course_id>/', views.student_course_detail, name='student-course-detail'),
    path('enroll/<int:course_id>/', views.student_enroll_course, name='student-enroll-course'),
    path('drop/<int:enrollment_id>/', views.drop_course, name='student-drop-course'),
    path('request-override/<int:course_id>/', views.student_request_override, name='student-request-override'),
    path('waitlist/<int:course_id>/', views.join_waitlist, name='waitlist_course'),
]