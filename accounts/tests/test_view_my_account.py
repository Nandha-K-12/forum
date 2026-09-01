from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..views import UserUpdateView


class UserUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='password123')
        self.url = reverse('my_account')

    def test_redirect_guest_user(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')

    def test_my_account_status_code(self):
        self.client.login(username='john', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_my_account_url_resolves_view(self):
        view = resolve('/accounts/settings/account/')
        self.assertEqual(view.func.view_class, UserUpdateView)

    def test_successful_profile_update(self):
        self.client.login(username='john', password='password123')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newjohn@doe.com'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'newjohn@doe.com')
