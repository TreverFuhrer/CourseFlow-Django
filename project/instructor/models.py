# instructor/models.py

from django.db import models
from project.administration.models import Course
from django.contrib.auth.models import User

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='instructors')

    def __str__(self):
        return f"Instructor: {self.user.username}"
