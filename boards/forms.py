from django import forms

from .models import Post, Topic


class TopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'placeholder': 'What do you want to discuss?'
            }
        )
    )

    class Meta:
        model = Topic
        fields = ['subject']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Reply to thread...',
                    'class': 'form-control form-control-threads'
                }
            )
        }