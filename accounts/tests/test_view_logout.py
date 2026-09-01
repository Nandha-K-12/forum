from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='password123')
        self.url = reverse('logout')

    def test_logout_status_code(self):
        self.client.login(username='john', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
