from django.test import TestCase

from ..forms import SignUpForm


class SignUpFormTests(TestCase):
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        expected_fields = ['username', 'email', 'password']
        self.assertSequenceEqual(list(form.fields.keys()), expected_fields)
