from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import ReplyTopicView


class ReplyTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='Lorem ipsum', topic=self.topic, created_by=self.user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})

    def test_reply_topic_redirect_guest_user(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')

    def test_reply_topic_success_status_code(self):
        self.client.login(username='john', password='123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_reply_topic_valid_post_data(self):
        self.client.login(username='john', password='123')
        data = {'message': 'This is a new reply message'}
        response = self.client.post(self.url, data)
        self.assertEqual(Post.objects.count(), 2)
        topic_posts_url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(response, topic_posts_url)

    def test_reply_topic_invalid_post_data(self):
        self.client.login(username='john', password='123')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
