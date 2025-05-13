from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Course, Enrollment, adminEmail

User = get_user_model()

# testing course stuff
class CourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = User.objects.create(username='daprof', password='testpass')

        # creating a course
        self.course = Course.objects.create(
            title='CS361',
            code='CS361',
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
            code='CS351',
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
        self.prof = User.objects.create(username='daprof', password='testpass', email='d@prof.com')
        self.student = User.objects.create(username='studenttt', password='testpass')
        self.course = Course.objects.create(
            title='CS361',
            code='CS361',
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
        self.prof = User.objects.create(username='daprof', password='testpass', email='d@prof.com')
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
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Welcome to the Enrollment Management System')

    def test_report_page(self):
        # test that report page loads and shows enrollment data
        self.client.logout()
        staff_user = User.objects.create_user(
            username='staffuser', 
            password='staffpass', 
            email='staff@example.com',
            is_staff=True
        )
        # Log in as staff user
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(reverse('report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report.html')
        self.assertContains(response, 'Enrollment Statistics')

    def test_report_redirect_if_not_staff(self):
        self.client.login(username='studenttt', password='testpass')
        response = self.client.get(reverse('report'))
        self.assertRedirects(response, reverse('home'))

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
        self.client = Client()
        self.client.login(username='admin', password='123456')

        # Set up test client

    def test_admin_login_success(self):
        """Test successful admin login"""
        # Login with admin credentials
        response = self.client.post(reverse('admin-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_home.html')
        self.assertContains(response, 'Courses')

    def test_admin_login_wrong_password(self):
        """Test admin login with wrong password"""
        # Attempt admin Login with wrong password
        self.client.logout()
        user = User.objects.create_user('test', 'tes@t.com', "pswd")
        self.client.login(username='test', password='pswd')
        response = self.client.get(reverse('admin-home'), follow=True)
        self.assertRedirects(response, reverse('student-dashboard'))



## this class will
# Admin Course management tests
class AdminCourseManagementTests(TestCase):
    def setUp(self):
        # create admin user for testing
        from django.contrib.auth.models import User

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gamil.com',
                password='123456'
            )

        # create instructor user
        self.instructor = User.objects.create(
            username='instructor',
            email='instructor@example.com',
            password='<111111>'
        )

        # test course
        self.course = Course.objects.create(
            title='TEST101',
            code='TEST101',
            description='This is a test course',
            seat_limit=30,
            instructor=self.instructor
        )

        # login as admin
        self.client = Client()
        self.client.login(username='admin', password='123456')


    def test_course_creation(self):
        """Test course creation through admin interface"""

        initial_count = Course.objects.count()

        course_data = {
            'title': 'Test Course',
            'description': 'This is a test course',
            'seat_limit': 30,
            'instructor': self.instructor.id
        }
        
        response = self.client.post(reverse('admin-course-add'), course_data, follow=True)

        # verify course was created
        self.assertEqual(Course.objects.count(), initial_count + 1)
        self.assertTrue(Course.objects.filter(title='Test Course').exists())

    def test_course_edit(self):
        """Test course edit through admin interface"""

        updated_data = {
            'title': 'Updated Course Title',
            'code': self.course.code,
            'description': 'Updated Course Description',
            'seat_limit': 35,
            'instructor': self.instructor.id
        }
        response = self.client.post(reverse('admin-course-edit', args=[self.course.id]), updated_data, follow=True)

        # verify course was updated
        updated_course = Course.objects.get(id=self.course.id)
        self.assertEqual(updated_course.title, 'Updated Course Title')
        self.assertEqual(updated_course.description, 'Updated Course Description')
        self.assertEqual(updated_course.seat_limit, 35)

    def test_course_prerequisites(self):
        """Test setting course prerequisites"""

        prereq_course = Course.objects.create(
            title='Prerequisites Course',
            description='This is Prerequisites Course',
            seat_limit=25,
            instructor=self.instructor
        )

        self.course.prerequisites.add(prereq_course)
        self.assertIn(prereq_course, self.course.prerequisites.all())

    def test_course_deletion(self):
        """Test course deletion through admin interface"""
        # count courses before deletion
        initial_count = Course.objects.count()

        response = self.client.post(f'/admin/administration/course/{self.course.id}/delete/', {'post': 'yes'}, follow=True)

        self.assertEqual(Course.objects.count(), initial_count - 1)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

# Admin Enrollment Management tests
class AdminEnrollmentTests(TestCase):
    def setUp(self):

        from django.contrib.auth.models import User

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gamil.com',
                password='123456'
            )
        # student user
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='<222222>'
        )

        # Instructor user
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='<333333>'
        )

        # test courses
        self.course = Course.objects.create(
            title='TEST101',
            description='This is a test course',
            seat_limit=30,
            instructor=self.instructor
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='pending'
        )

        self.client = Client()
        self.client.login(username='admin', password='123456')


    def test_approve_enrollment(self):
        """Test approving student enrollment"""

        enrollment_data = {
            'student': self.student.id,
            'course': self.course.id,
            'status': 'approved'
        }

        # Update enrollment through admin interface
        response = self.client.post(f'/admin/administration/enrollment/{self.enrollment.id}/change/', enrollment_data, follow=True)

        # verify enorllmment was approved
        updated_enrollment = Enrollment.objects.get(id=self.enrollment.id)
        self.assertEqual(updated_enrollment.status, 'approved')

    def test_reject_enrollment(self):
        """Test rejecting student enrollment"""
        enrollment_data = {
            'student': self.student.id,
            'course': self.course.id,
            'status': 'rejected'
        }

        #update
        response = self.client.post(f'/admin/administration/enrollment/{self.enrollment.id}/change/', enrollment_data, follow=True)

        updated_enrollment = Enrollment.objects.get(id=self.enrollment.id)
        self.assertEqual(updated_enrollment.status, 'rejected')


# Admin Email Tests
class AdminEmailTests(TestCase):
    def setUp(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admi@n.com', '123456')
        self.client = Client()
        self.client.login(username='admin', password='123456')

    def test_email_page(self):
        response = self.client.get(reverse('admin-email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/email.html')
        self.assertContains(response, 'Write New Email')

    def test_send_email(self):
        before = adminEmail.objects.count()
        data = {'email': 'x@y.com', 'subject': 'S', 'message': 'M'}
        response = self.client.post(reverse('admin-email'), data, follow=True)
        self.assertEqual(adminEmail.objects.count(), before + 1)
        self.assertContains(response, 'S')

