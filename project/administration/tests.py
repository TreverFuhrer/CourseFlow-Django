from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = User.objects.create(username='daprof', password='testpass')
