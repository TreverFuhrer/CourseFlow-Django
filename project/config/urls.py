"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


import advisor
from administration.views import home, report, email, admin_home
from advisor.views import advisor_home, send_message, view_conversation, advisor_list
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from administration.views import course_create, course_update, course_delete,override_action, student_detail
from administration.views import student_dashboard
from advisor.views import advisor_detail, enrollment_action
from student.views import student_dashboard,student_course_search,student_all_courses,student_course_detail,student_enroll_course,drop_course,student_request_override,join_waitlist
# If this doesn't work right click project folder
# Mark directory as source
# File, invalidate caches, restart pycharm


urlpatterns = [
    path('', home, name='home'),

    # login/logout just redirects to home
    path('login/', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # admin dashboard
    path('admin-home/', login_required(admin_home), name='admin-home'),

    # student dashboard
    path('student-home/',                 login_required(student_dashboard),             name='student-dashboard'),
    path('search-classes/',               login_required(student_course_search),         name='student-class-search'),
    path('all-courses/',                  login_required(student_all_courses),           name='student-view-all-courses'),
    path('class/<int:course_id>/',        login_required(student_course_detail),         name='student-course-detail'),
    path('enroll/<int:course_id>/',       login_required(student_enroll_course),         name='student-enroll-course'),
    path('drop/<int:enrollment_id>/',     login_required(drop_course),                  name='student-drop-course'),
    path('request-override/<int:course_id>/', login_required(student_request_override),    name='student-request-override'),
    path('waitlist/<int:course_id>/',     login_required(join_waitlist),                name='waitlist_course'),

    # Course Stuff for admin
    path('admin-home/courses/add/',     course_create, name='admin-course-add'),
    path('admin-home/courses/<int:pk>/edit/',   course_update, name='admin-course-edit'),
    path('admin-home/courses/<int:pk>/delete/', course_delete, name='admin-course-delete'),

    # override approvals for admin
    path('admin-home/overrides/<int:pk>/action/', override_action, name='admin-override-action'),

    # student management for admin
    path('admin-home/students/<int:pk>/', student_detail, name='admin-student-detail'),

    # admin report and email
    path('report/', report, name='report'),
    path('admin/email/', email, name='admin-email'),

    # backend admin
    path('admin/', admin.site.urls),

    # advisor homepage
    path('advisor-home/', login_required(advisor_home), name='advisor-home'),

    # advisor student info
    path('advisor-home/students/<int:pk>/', advisor_detail, name='advisor-student-detail'),

    # advisor chat
    path('advisor_list/', advisor_list, name='advisor_list'),
    path('conversation/<int:recipient_id>/', login_required(view_conversation), name='view_conversation'),path('send/<int:recipient_id>/', login_required(send_message), name='send_message'),
    path('chat/conversation/<int:recipient_id>/', login_required(view_conversation), name='view_conversation'),
    path('chat/send/<int:recipient_id>/', login_required(send_message), name='send_message'),

    #Advisor Admin functions
    path('advisor-home/students/<int:pk>/', advisor_detail, name='advisor-student-detail'),
    path('advisor-home/enrollment/<int:enr_id>/action/',enrollment_action,name='advisor-enrollment-action'),
]

