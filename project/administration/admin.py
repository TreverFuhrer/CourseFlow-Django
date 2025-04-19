from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Course, Enrollment
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'seat_limit', 'remove')

    def remove(self, obj):
        url = reverse('admin:administration_course_delete', args=[obj.pk])
        return format_html('<a style="color:#9E1A1A;" href="{}">Remove</a>', url)

class EnrollmentInLine(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('course', 'status', 'enrollment_date')
    fields = readonly_fields

class StudentAdmin(UserAdmin):
    inlines = [EnrollmentInLine]
    ordering = ('username',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active')
    list_filter = ('is_active',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)

admin.site.unregister(User)
admin.site.register(User, StudentAdmin)

admin.site.register(Enrollment)
