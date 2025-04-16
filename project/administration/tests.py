from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Course, Enrollment

User = get_user_model()

# testing course stuff
class CourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = User.objects.create(username='daprof', password='testpass')

        # creating a course
        self.course = Course.objects.create(
            title='CS361',
            description='Software Engineering',
            seat_limit=30,
            instructor=self.prof
        )

    def test_course_str_returns_title(self):
        # __str__ should just be the course title
        self.assertEqual(str(self.course), 'CS361')

    def test_can_add_prereq_to_course(self):
        # add a prereq to the course and check it's there
        prereq = Course.objects.create(
            title='CS351',
            description='Data Structures',
            seat_limit=30,
            instructor=self.prof
        )
        self.course.prerequisites.add(prereq)
        self.assertIn(prereq, self.course.prerequisites.all())

# testing enrollments
class EnrollmentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = User.objects.create(username='daprof', password='testpass')
        self.student = User.objects.create(username='studenttt', password='testpass')
        self.course = Course.objects.create(
            title='CS361',
            description='Software Engineering',
            seat_limit=30,
            instructor=self.prof
        )

        # enroll the student in the course
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )

    def test_enrollment_str_format(self):
        # should return something like "studenttt - CS361"
        self.assertEqual(str(self.enrollment), f"{self.student} - {self.course}")

    def test_default_status_is_pending(self):
        # when you enroll, it should start as "pending"
        self.assertEqual(self.enrollment.status, 'pending')

# testing homepage and report page
class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = User.objects.create(username='daprof', password='testpass')
        self.student = User.objects.create(username='studenttt', password='testpass')
        self.course = Course.objects.create(
            title='CS361',
            description='Software Engineering',
            seat_limit=30,
            instructor=self.prof
        )

        # give some enrollments different statuses
        Enrollment.objects.create(student=self.student, course=self.course, status='approved')
        Enrollment.objects.create(student=self.student, course=self.course, status='pending')

    def test_homepage(self):
        response = self.client.get('/')

    def test_report_page(self):
        response = self.client.get('/report/')