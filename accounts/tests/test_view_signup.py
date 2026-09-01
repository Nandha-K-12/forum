from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import SignUpForm
from ..views import SignUpView


class SignUpTests(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.view_class, SignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_valid_post_data(self):
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password': 'password123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='john').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_post_data(self):
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(User.objects.exists())

    def test_invalid_post_data_empty_fields(self):
        data = {
            'username': '',
            'email': '',
            'password': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())
