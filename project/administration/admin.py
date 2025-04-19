from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Course, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'seat_limit', 'remove')

    def remove(self, obj):
        url = reverse('admin:administration_course_delete', args=[obj.pk])
        return format_html('<a style="color:#9E1A1A;" href="{}">Remove</a>', url)

admin.site.register(Enrollment)
