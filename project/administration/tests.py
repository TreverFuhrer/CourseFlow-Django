from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()

class CourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = User.objects.create(username='daprof', password='testpass')
        self.course = Course.objects.create(
            title='CS361',
            description='Software Engineering',
            seat_limit=30,
            instructor=self.prof
        )

    def test_course_str_returns_title(self):
        self.assertEqual(str(self.course), 'CS361')

    def test_can_add_prereq_to_course(self):
        prereq = Course.objects.create(
            title='CS351',
            description='Data Structures',
            seat_limit=30,
            instructor=self.prof
        )
        self.course.prerequisites.add(prereq)
        self.assertIn(prereq, self.course.prerequisites.all())
