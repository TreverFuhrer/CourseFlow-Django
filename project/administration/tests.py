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
        # test that homepage loads and has expected content
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Welcome to the Enrollment Management System')
        self.assertContains(response, 'Username:')
        self.assertContains(response, 'Sign in as Admin')

    def test_report_page(self):
        # test that report page loads and shows enrollment data
        response = self.client.get('/report/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report.html')
        self.assertContains(response, 'Enrollment Statistics')
        self.assertContains(response, 'Total Courses Offered')
        self.assertContains(response, 'Total Class Enrollment')
        self.assertContains(response, 'Approved')
        self.assertContains(response, 'Pending')
        self.assertContains(response, 'Back to Admin')

class AdminAcceptanceTests(TestCase):
    def setUp(self):
        # create an admin user for testing
        from django.contrib.auth.models import User

        # use the existing admin from admin.py
        if not User.objects.filter(username='admin').exists():
           User.objects.create_superuser(
               username='admin',
               email='admin@gamil.com',
               password='123456'
           )

        # Set up test client
        self.client = Client()

    def test_admin_login_success(self):
        """Test successful admin login"""
        # Login with admin credentials
        login_successful = self.client.login(username='admin', password='123456')
        self.assertTrue(login_successful)

        # access admin page after Login
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_wrong_password(self):
        """Test admin login with wrong password"""
        # Attempt admin Login with wrong password
        login_successful = self.client.login(username='admin', password='wrong password')
        self.assertFalse(login_successful)

        

