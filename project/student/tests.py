from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from administration.models import Course, Enrollment, OverrideRequest

User = get_user_model()

class StudentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='teststudent', password='password123')
        self.course = Course.objects.create(title='TEST101', seat_limit=30)


    def test_student_dashboard_requires_login(self):
        response = self.client.get(reverse('student-dashboard'))
        self.assertRedirects(response, '/login/?next=' + reverse('student-dashboard'))


    def test_student_dashboard_displays_enrollments(self):
        Enrollment.objects.create(course=self.course, student=self.student, status='enrolled')
        self.client.login(username='teststudent', password='password123')

        response = self.client.get(reverse('student-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST101')  # Checking if course name appears


    def test_student_enroll_in_course_get(self):
        self.client.login(username='teststudent', password='password123')

        response = self.client.get(reverse('student-enroll-course', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/enroll_confirm.html')

    def test_student_enroll_in_course_post(self):
        self.client.login(username='teststudent', password='password123')

        response = self.client.post(reverse('student-enroll-course', args=[self.course.id]))
        self.assertRedirects(response, reverse('student-dashboard'))

        enrollment_exists = Enrollment.objects.filter(course=self.course, student=self.student).exists()
        self.assertTrue(enrollment_exists)

    def test_student_enroll_in_course_already_enrolled(self):
        Enrollment.objects.create(course=self.course, student=self.student, status='enrolled')
        self.client.login(username='teststudent', password='password123')

        response = self.client.post(reverse('student-enroll-course', args=[self.course.id]))
        self.assertRedirects(response, reverse('student-dashboard'))

        enrollment_count = Enrollment.objects.filter(course=self.course, student=self.student).count()
        self.assertEqual(enrollment_count, 1)  # No duplicate enrollments

    def test_student_request_override_get(self):
        self.client.login(username='teststudent', password='password123')

        response = self.client.get(reverse('student-request-override', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/override_request.html')

    def test_student_request_override_post(self):
        self.client.login(username='teststudent', password='password123')

        response = self.client.post(reverse('student-request-override', args=[self.course.id]), {
            'reason': 'Schedule conflict'
        })
        self.assertRedirects(response, reverse('student-dashboard'))

        override_exists = OverrideRequest.objects.filter(course=self.course, student=self.student, reason='Schedule conflict').exists()
        self.assertTrue(override_exists)


    def test_student_drop_course(self):
        Enrollment.objects.create(course=self.course, student=self.student, status='enrolled')
        self.client.login(username='teststudent', password='password123')
        response = self.client.post(reverse('student-drop-course', args=[self.course.id]))
        self.assertRedirects(response, reverse('student-dashboard'))
        self.assertFalse(Enrollment.objects.filter(course=self.course, student=self.student).exists())

    def test_view_all_courses(self):
        self.client.login(username='teststudent', password='password123')
        response = self.client.get(reverse('student-view-all-courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST101')

    def test_search_course_by_title(self):
        self.client.login(username='teststudent', password='password123')
        response = self.client.get(reverse('student-class-search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST101')
