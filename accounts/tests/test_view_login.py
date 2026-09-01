from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..views import SignInView


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='password123')
        self.url = reverse('login')

    def test_login_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func.view_class, SignInView)

    def test_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_successful_login(self):
        data = {'username': 'john', 'password': 'password123'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_unsuccessful_login(self):
        data = {'username': 'john', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
