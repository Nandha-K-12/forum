from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('boards/<int:pk>/', views.BoardTopicsView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.NewTopicView.as_view(), name='new_topic'),
    path(
        'boards/<int:pk>/topics/<int:topic_pk>/',
        views.TopicPostsView.as_view(),
        name='topic_posts'
    ),
    path(
        'boards/<int:pk>/topics/<int:topic_pk>/reply/',
        views.ReplyTopicView.as_view(),
        name='reply_topic'
    ),
    path(
        'boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
]