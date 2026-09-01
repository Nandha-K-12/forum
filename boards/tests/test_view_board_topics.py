from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board
from ..views import BoardTopicsView


class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve(f'/boards/{self.board.pk}/')
        self.assertEqual(view.func.view_class, BoardTopicsView)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})

        response = self.client.get(board_topics_url)
        self.assertContains(response, f'href="{homepage_url}"')
        self.assertContains(response, f'href="{new_topic_url}"')
