from django.test import TestCase
from django.contrib.auth.models import User
from project.administration.models import Course, Enrollment, OverrideRequest
from .models import InstructorProfile

class InstructorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='instructor1', password='pass1234')
        self.course = Course.objects.create(title='Test Course', description='Test Description', seat_limit=30)
        self.instructor_profile = InstructorProfile.objects.create(user=self.user)
        self.instructor_profile.courses.add(self.course)

    def test_instructor_profile_creation(self):
        self.assertEqual(self.instructor_profile.user.username, 'instructor1')
        self.assertIn(self.course, self.instructor_profile.courses.all())

class InstructorViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testinstructor', password='testpassword')
        self.course = Course.objects.create(
            title='361',
            description='Software Engineering',
            seat_limit=30,
            instructor=self.user
        )
        self.student = User.objects.create_user(username='teststudent', password='testpassword')
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.student, status='pending')
        self.override_request = OverrideRequest.objects.create(course=self.course, student=self.student, status='pending')
        self.client.login(username='testinstructor', password='testpassword')

    def test_instructor_dashboard_view(self):
        response = self.client.get('/instructor/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_manage_enrollments_view(self):
        response = self.client.get(f'/instructor/manage_enrollments/{self.course.id}/')
        self.assertEqual(response.status_code, 200)

    def test_approve_enrollment(self):
        response = self.client.post(f'/instructor/approve_enrollment/{self.enrollment.id}/')
        self.enrollment.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.enrollment.status, 'approved')

    def test_reject_enrollment(self):
        response = self.client.post(f'/instructor/reject_enrollment/{self.enrollment.id}/')
        self.enrollment.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.enrollment.status, 'rejected')

    def test_approve_override_request(self):
        response = self.client.post(f'/instructor/approve_override/{self.override_request.id}/')
        self.override_request.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.override_request.status, 'approved')

    def test_reject_override_request(self):
        response = self.client.post(f'/instructor/reject_override/{self.override_request.id}/')
        self.override_request.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.override_request.status, 'rejected')

    def test_update_course_details(self):
        response = self.client.post(f'/instructor/update_course/{self.course.id}/', {
            'title': '371',
            'description': 'New course description!!',
            'seat_limit': 50,
        })
        self.course.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.title, '371')
        self.assertEqual(self.course.description, 'New course description!!')
        self.assertEqual(self.course.seat_limit, 50)
