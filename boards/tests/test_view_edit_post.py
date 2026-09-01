from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import PostUpdateView


class PostUpdateViewTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='Lorem ipsum', topic=self.topic, created_by=self.user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })

    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')

    def test_status_code(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_post_update_view(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/posts/{self.post.pk}/edit/')
        self.assertEqual(view.func.view_class, PostUpdateView)

    def test_post_update_valid_data(self):
        self.client.login(username=self.username, password=self.password)
        data = {'message': 'Updated message'}
        response = self.client.post(self.url, data)
        self.post.refresh_from_db()
        self.assertEqual(self.post.message, 'Updated message')
        topic_posts_url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(response, topic_posts_url)
