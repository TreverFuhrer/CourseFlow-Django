from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse

from administration.models import Course, Enrollment, OverrideRequest

class InstructorTests(TestCase):
    def setUp(self):
        # Create the Instructor group
        self.instructor_group = Group.objects.create(name='Instructor')

        # Create an instructor and add to the group
        self.instructor = User.objects.create_user(
            username='alexander789', password='passWord'
        )
        self.instructor.groups.add(self.instructor_group)

        # Create a course assigned to the instructor
        self.course = Course.objects.create(
            title='789',
            description='yoooooo',
            seat_limit=30,
            instructor=self.instructor
        )

        # Create a student and an enrollment
        self.student = User.objects.create_user(
            username='michael456', password='passWord', email='mike@example.com'
        )
        self.enrollment = Enrollment.objects.create(
            course=self.course,
            student=self.student,
            status='pending'
        )

        # Create a pending override request
        self.override_request = OverrideRequest.objects.create(
            student=self.student,
            course=self.course,
            reason='I need an override'
        )

        # Log in as the instructor for each test
        self.client.login(username='alexander789', password='passWord')

    # ---- Dashboard & Enrollments ----

    def test_instructor_dashboard_view(self):
        resp = self.client.get(reverse('instructor:instructor-dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.course.title)
        self.assertContains(resp, self.instructor.username)

    def test_manage_enrollments_view(self):
        resp = self.client.get(
            reverse('instructor:instructor-manage-enrollments', args=[self.course.id])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.student.username)

    def test_dashboard_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse('instructor:instructor-dashboard'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_manage_enrollments_requires_login(self):
        self.client.logout()
        resp = self.client.get(
            reverse('instructor:instructor-manage-enrollments', args=[self.course.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_enrollment_restriction_for_non_instructor(self):
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        resp = self.client.get(
            reverse('instructor:instructor-manage-enrollments', args=[self.course.id])
        )
        self.assertEqual(resp.status_code, 404)

    # ---- Approve / Reject Enrollments ----

    def test_approve_enrollment(self):
        resp = self.client.post(
            reverse('instructor:instructor-approve-enrollment', args=[self.enrollment.id])
        )
        self.enrollment.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.enrollment.status, 'approved')

    def test_reject_enrollment(self):
        resp = self.client.post(
            reverse('instructor:instructor-reject-enrollment', args=[self.enrollment.id])
        )
        self.enrollment.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.enrollment.status, 'rejected')

    def test_only_instructor_can_approve_reject(self):
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        resp = self.client.post(
            reverse('instructor:instructor-approve-enrollment', args=[self.enrollment.id])
        )
        self.assertEqual(resp.status_code, 403)
        resp = self.client.post(
            reverse('instructor:instructor-reject-enrollment', args=[self.enrollment.id])
        )
        self.assertEqual(resp.status_code, 403)

    # ---- Update Course ----

    def test_update_course_details(self):
        resp = self.client.post(
            reverse('instructor:instructor-update-course', args=[self.course.id]),
            {
                'title': 'Updated Course',
                'description': 'Updated Description',
                'seat_limit': 50,
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course')
        self.assertEqual(self.course.description, 'Updated Description')
        self.assertEqual(self.course.seat_limit, 50)

    def test_update_course_permission(self):
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        resp = self.client.post(
            reverse('instructor:instructor-update-course', args=[self.course.id]),
            {
                'title': 'Malicious',
                'description': 'Nope',
                'seat_limit': 1
            }
        )
        self.assertEqual(resp.status_code, 404)
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.title, 'Malicious')

    def test_update_course_requires_login(self):
        self.client.logout()
        resp = self.client.get(
            reverse('instructor:instructor-update-course', args=[self.course.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    # ---- Override Requests ----

    def test_override_requests_view(self):
        resp = self.client.get(reverse('instructor:instructor-override-requests'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.student.username)
        self.assertContains(resp, self.course.title)

    def test_override_requests_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse('instructor:instructor-override-requests'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_approve_override(self):
        resp = self.client.post(
            reverse('instructor:instructor-approve-override', args=[self.override_request.id])
        )
        self.override_request.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.override_request.status, 'approved')

    def test_reject_override(self):
        resp = self.client.post(
            reverse('instructor:instructor-reject-override', args=[self.override_request.id])
        )
        self.override_request.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.override_request.status, 'rejected')

    def test_override_permission(self):
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        resp = self.client.post(
            reverse('instructor:instructor-approve-override', args=[self.override_request.id])
        )
        self.assertEqual(resp.status_code, 404)

    # ---- Email Student ----

    def test_email_student_view_get(self):
        resp = self.client.get(
            reverse('instructor:instructor-email-student', args=[self.enrollment.id])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<form')
        self.assertContains(resp, 'name="subject"')
        self.assertContains(resp, 'name="message"')

    def test_email_student_post(self):
        resp = self.client.post(
            reverse('instructor:instructor-email-student', args=[self.enrollment.id]),
            {'subject': 'Test', 'message': 'Hello there'}
        )
        self.assertEqual(resp.status_code, 302)

    def test_email_student_requires_login(self):
        self.client.logout()
        resp = self.client.get(
            reverse('instructor:instructor-email-student', args=[self.enrollment.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_email_student_permission(self):
        self.client.logout()
        self.client.login(username='michael456', password='passWord')
        resp = self.client.get(
            reverse('instructor:instructor-email-student', args=[self.enrollment.id])
        )
        self.assertEqual(resp.status_code, 404)