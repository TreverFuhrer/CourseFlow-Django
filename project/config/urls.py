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
from django.urls import path

import advisor
from administration.views import home, report, email, admin_home
from advisor.views import advisor_home, send_message, view_conversation, advisor_list
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from administration.views import course_create, course_update, course_delete,override_action, student_detail
from administration.views import student_dashboard
# If this doesn't work right click project folder
# Mark directory as source
# File, invalidate caches, restart pycharm




app_name = 'chat'

urlpatterns = [
    path('', home, name='home'),

    # login/logout just redirects to home
    path('login/', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # admin dashboard
    path('admin-home/', login_required(admin_home), name='admin-home'),

    # student dashboard
    #TODO implement this
    path('student-home/', login_required(student_dashboard), name='student-dashboard'),

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

    # advisor/chat
    path('advisor/', advisor_list, name='advisor_list'),
    path('conversation/<int:recipient_id>/', view_conversation, name='view_conversation'),
    path('send/<int:recipient_id>/', send_message, name='send_message'),
]
