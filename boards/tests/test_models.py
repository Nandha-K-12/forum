from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Board, Post, Topic


class ModelTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='Lorem ipsum', topic=self.topic, created_by=self.user)

    def test_board_str(self):
        self.assertEqual(str(self.board), 'Django')

    def test_topic_str(self):
        self.assertEqual(str(self.topic), 'Hello, world')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Lorem ipsum')

    def test_board_get_posts_count(self):
        self.assertEqual(self.board.get_posts_count(), 1)

    def test_board_get_last_post(self):
        self.assertEqual(self.board.get_last_post(), self.post)
