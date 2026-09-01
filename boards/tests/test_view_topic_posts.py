from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import TopicPostsView


class TopicPostsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        Post.objects.create(message='Lorem ipsum', topic=self.topic, created_by=self.user)
        self.url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/')
        self.assertEqual(view.func.view_class, TopicPostsView)

    def test_view_count_increment(self):
        self.assertEqual(self.topic.views, 0)
        self.client.get(self.url)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.views, 1)
