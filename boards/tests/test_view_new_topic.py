from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import TopicForm
from ..models import Board, Post, Topic
from ..views import NewTopicView


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})

    def test_new_topic_view_success_status_code(self):
        self.client.login(username='john', password='123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        self.client.login(username='john', password='123')
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve(f'/boards/{self.board.pk}/new/')
        self.assertEqual(view.func.view_class, NewTopicView)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        self.client.login(username='john', password='123')
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(self.url)
        self.assertContains(response, f'href="{board_topics_url}"')

    def test_csrf(self):
        self.client.login(username='john', password='123')
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        self.client.login(username='john', password='123')
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertIsInstance(form, TopicForm)

    def test_new_topic_valid_post_data(self):
        self.client.login(username='john', password='123')
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
        topic = Topic.objects.first()
        self.assertRedirects(response, reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': topic.pk}))

    def test_new_topic_invalid_post_data(self):
        self.client.login(username='john', password='123')
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        self.client.login(username='john', password='123')
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_new_topic_redirect_guest_user(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')
