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
        self.user = User.objects.create_user(username='instructor2', password='pass1234')
        self.course = Course.objects.create(title='Another Course', description='Another Description', seat_limit=25, instructor=self.user)
        self.client.login(username='instructor2', password='pass1234')

    def test_instructor_dashboard_view(self):
        response = self.client.get('/instructor/dashboard/')  # Adjust URL if needed
        self.assertEqual(response.status_code, 200)

    def test_manage_enrollments_view(self):
        response = self.client.get(f'/instructor/manage_enrollments/{self.course.id}/')  # Adjust URL if needed
        self.assertEqual(response.status_code, 200)

    # TODO: Test approving enrollment
    # def test_approve_enrollment(self):
    #     pass

    # TODO: Test rejecting enrollment
    # def test_reject_enrollment(self):
    #     pass

    # TODO: Test override request approval
    # def test_approve_override_request(self):
    #     pass

    # TODO: Test override request rejection
    # def test_reject_override_request(self):
    #     pass

    # TODO: Test updating course details
    # def test_update_course_details(self):
    #     pass
