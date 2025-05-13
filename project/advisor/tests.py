from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse

from administration.models import Course, Enrollment
from advisor.models import Message

class AdvisorTests(TestCase):
    def setUp(self):
        self.advisor_group = Group.objects.create(name='Advisor')
        self.student_group = Group.objects.create(name='Student')

        self.advisor = User.objects.create_user(username='advisoruser', password='advpass')
        self.advisor.groups.add(self.advisor_group)
        self.student = User.objects.create_user(username='studentuser', password='stupass', email='student@example.com')
        self.student.groups.add(self.student_group)
        self.instructor = User.objects.create_user(username='instructoruser', password='inspass')

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            seat_limit=30,
            instructor=self.instructor
        )

        self.enrollment = Enrollment.objects.create(
            course=self.course,
            student=self.student,
            status='pending'
        )

        self.client.login(username='advisoruser', password='advpass')

    def test_student_detail_view(self):
        resp = self.client.get(reverse('advisor-student-detail', args=[self.student.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.student.username)
        self.assertContains(resp, self.course.title)

    def test_dashboard_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse('advisor-home'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_student_detail_requires_login(self):
        self.client.logout()
        resp = self.client.get(
            reverse('advisor-student-detail', args=[self.student.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_advisor_permission_restriction(self):
        self.client.logout()
        self.client.login(username='studentuser', password='stupass')
        resp = self.client.get(reverse('advisor-home'))
        self.assertEqual(resp.status_code, 302)

    def test_approve_enrollment(self):
        resp = self.client.post(
            reverse('advisor-enrollment-action', args=[self.enrollment.id]),{'action': 'approve'})
        self.enrollment.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.enrollment.status, 'approved')

    def test_reject_enrollment(self):
        resp = self.client.post(
            reverse('advisor-enrollment-action', args=[self.enrollment.id]),{'action': 'reject'})
        self.enrollment.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.enrollment.status, 'rejected')

    def test_student_access_restriction(self):
        self.client.logout()
        self.client.login(username='studentuser', password='stupass')
        resp = self.client.post(reverse('advisor-enrollment-action', args=[self.enrollment.id]),{'action': 'approve'})
        self.assertEqual(resp.status_code, 302)
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'pending')

    def test_advisor_list_view(self):
        resp = self.client.get(reverse('advisor_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.student.username)

    def test_advisor_list_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse('advisor_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/login/'))

    def test_send_message(self):
        initial_count = Message.objects.count()
        resp = self.client.post(
            reverse('send_message', args=[self.student.id]),{'content': 'Test message'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Message.objects.count(), initial_count + 1)
        self.assertEqual(Message.objects.last().content, 'Test message')

    def test_view_conversation(self):
        Message.objects.create(
            sender=self.advisor,
            recipient=self.student,
            content='Hello student'
        )
        Message.objects.create(
            sender=self.student,
            recipient=self.advisor,
            content='Hello advisor'
        )
        resp = self.client.get(reverse('view_conversation', args=[self.student.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello student')
        self.assertContains(resp, 'Hello advisor')
