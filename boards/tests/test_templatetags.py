from django.contrib.auth.models import User
from django.test import TestCase

from ..templatetags.gravatar import gravatar
from ..templatetags.markdown_tags import render_markdown


class GravatarTests(TestCase):
    def test_gravatar_url_generation(self):
        user = User(username='johndoe', email='john@example.com')
        url = gravatar(user)
        self.assertIn('gravatar.com/avatar/', url)
        self.assertIn('d=mm', url)

    def test_gravatar_empty_email(self):
        user = User(username='noemail', email='')
        url = gravatar(user)
        self.assertIn('gravatar.com/avatar/', url)


class MarkdownTests(TestCase):
    def test_render_markdown(self):
        plain_text = '**Bold text** and *italic text*'
        html = render_markdown(plain_text)
        self.assertIn('<strong>Bold text</strong>', html)
        self.assertIn('<em>italic text</em>', html)

    def test_render_empty(self):
        self.assertEqual(render_markdown(''), '')
