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
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from administration.views import home, report, email
from advisor.views import send_message, view_conversation, advisor_list
from django.contrib.auth.decorators import login_required
# If this doesn't work right click project folder
# Mark directory as source
# File, invalidate caches, restart pycharm

app_name = 'chat'

urlpatterns = [
    path('', home, name='home'),
    path('report/', report, name='report'),
    path('admin/email/', staff_member_required(email), name='admin-email'),
    path('admin/', admin.site.urls),
    path('advisor/', advisor_list, name='advisor_list'),
    path('conversation/<int:recipient_id>/', view_conversation, name='view_conversation'),
    path('send/<int:recipient_id>/', send_message, name='send_message'),
]
