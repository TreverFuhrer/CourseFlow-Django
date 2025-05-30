from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, default='UNKN101')
    description = models.TextField()
    seat_limit = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, related_name='courses')

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        return self.enrollments.count() >= self.seat_limit

    def missing_prerequisites(self, student):
        taken = {enrolled.course for enrolled in student.enrollments.all()}
        return self.prerequisites.exclude(pk__in=[c.pk for c in taken])

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

#Same as Enrollment
#TODO implemnt this
class OverrideRequest(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='override_requests'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='override_requests'
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending'
    )
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.status})"

class adminEmail(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.date:%Y-%M-%D} -> {self.email}"