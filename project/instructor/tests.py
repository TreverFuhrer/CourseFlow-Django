from django.test import TestCase
from django.contrib.auth.models import User, Group
from administration.models import Course, Enrollment, OverrideRequest
from django.urls import reverse


class InstructorTests(TestCase):
    def setUp(self):
        # Create the Instructor group
        self.instructor_group = Group.objects.create(name='Instructor')

        # Create an instructor and add to the group
        self.instructor = User.objects.create_user(username='alexander789', password='passWord')
        self.instructor.groups.add(self.instructor_group)

        # Create a course assigned to the instructor
        self.course = Course.objects.create(
            title='789',
            description='yoooooo',
            seat_limit=30,
            instructor=self.instructor
        )

        # Create a student and an enrollment
        self.student = User.objects.create_user(username='michael456', password='passWord')
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.student, status='pending')

        # Log in as the instructor for each test
        self.client.login(username='alexander789', password='passWord')

    def test_instructor_dashboard_view(self):
        response = self.client.get(reverse('instructor:instructor-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '789')
        self.assertContains(response, self.instructor.username)

    def test_manage_enrollments_view(self):
        response = self.client.get(reverse('instructor:instructor-manage-enrollments', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '789')
        self.assertContains(response, self.student.username)

    def test_approve_enrollment(self):
        response = self.client.post(reverse('instructor:instructor-approve-enrollment', args=[self.enrollment.id]))
        self.enrollment.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.enrollment.status, 'approved')

    def test_reject_enrollment(self):
        response = self.client.post(reverse('instructor:instructor-reject-enrollment', args=[self.enrollment.id]))
        self.enrollment.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.enrollment.status, 'rejected')

    def test_update_course_details(self):
        response = self.client.post(reverse('instructor:instructor-update-course', args=[self.course.id]), {
            'title': 'Updated Course',
            'description': 'Updated Description',
            'seat_limit': 50,
        })
        self.course.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.title, 'Updated Course')
        self.assertEqual(self.course.description, 'Updated Description')
        self.assertEqual(self.course.seat_limit, 50)

    def test_enrollment_restriction_for_non_instructor(self):
        # Log out the instructor and log in as a student
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        response = self.client.get(reverse('instructor:instructor-manage-enrollments', args=[self.course.id]))
        self.assertNotEqual(response.status_code, 200)  # Should be forbidden

    def test_only_instructor_can_approve_reject(self):
        # Log out the instructor and log in as a student
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        response = self.client.post(reverse('instructor:instructor-approve-enrollment', args=[self.enrollment.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_update_course_permission(self):
        # Log out the instructor and log in as a student
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        response = self.client.post(reverse('instructor:instructor-update-course', args=[self.course.id]), {
            'title': 'Malicious Update',
            'description': 'Unauthorized Change',
            'seat_limit': 5,
        })
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.title, 'Malicious Update')  # Should not allow this update

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('instructor:instructor-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith('/login/'))

    def test_manage_enrollments_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('instructor:instructor-manage-enrollments', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith('/login/'))