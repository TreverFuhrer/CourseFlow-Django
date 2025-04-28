from django.contrib import admin
from .models import InstructorProfile

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')


### Test instructor login
# Username:
# Trever

# Password
# Instructor