from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView

from .forms import PostForm, TopicForm
from .models import Board, Post, Topic


class HomeView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


class BoardTopicsView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 10

    def get_queryset(self):
        board_pk = self.kwargs.get('pk') or self.kwargs.get('board_id')
        self.board = get_object_or_404(Board, pk=board_pk)
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context


class TopicPostsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 10

    def get_queryset(self):
        board_pk = self.kwargs.get('pk') or self.kwargs.get('board_id')
        topic_pk = self.kwargs.get('topic_pk') or self.kwargs.get('topic_id')
        self.topic = get_object_or_404(
            Topic,
            board__pk=board_pk,
            pk=topic_pk
        )
        session_key = f'viewed_topic_{self.topic.pk}'
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        return self.topic.posts.order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        context['form'] = PostForm()
        return context


class NewTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'boards/new_topic.html'

    def dispatch(self, request, *args, **kwargs):
        board_pk = self.kwargs.get('pk') or self.kwargs.get('board_id')
        self.board = get_object_or_404(Board, pk=board_pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.board = self.board
        topic.starter = self.request.user
        topic.last_updated = timezone.now()
        topic.save()

        Post.objects.create(
            topic=topic,
            message=form.cleaned_data['message'],
            created_by=self.request.user,
        )

        return redirect(
            'topic_posts',
            pk=self.board.pk,
            topic_pk=topic.pk,
        )


class ReplyTopicView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'boards/reply_topic.html'

    def dispatch(self, request, *args, **kwargs):
        board_pk = self.kwargs.get('pk') or self.kwargs.get('board_id')
        topic_pk = self.kwargs.get('topic_pk') or self.kwargs.get('topic_id')
        self.topic = get_object_or_404(
            Topic,
            board__pk=board_pk,
            pk=topic_pk
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.topic = self.topic
        post.created_by = self.request.user
        post.save()

        self.topic.last_updated = timezone.now()
        self.topic.save()

        return redirect(
            'topic_posts',
            pk=self.topic.board.pk,
            topic_pk=self.topic.pk,
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        post.topic.last_updated = timezone.now()
        post.topic.save()

        return redirect(
            'topic_posts',
            pk=post.topic.board.pk,
            topic_pk=post.topic.pk,
        )
