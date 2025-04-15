from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    seat_limit = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
    )

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    STATUS_OPTIONS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='pending')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"