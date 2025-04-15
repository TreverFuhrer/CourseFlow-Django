from django.contrib import admin
from .models import Course, Enrollment

'''
Admin Login
username: admin
email: admin@gmail.com
password: 123456
'''

# Register your models here.
admin.site.register(Course)

admin.site.register(Enrollment)