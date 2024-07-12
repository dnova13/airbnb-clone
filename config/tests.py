from django.test import TestCase
from django.urls import reverse

class ProjectLevelTest(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('core:home')) # = response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Welcome to My Project")
        
        
        