from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    评论  表单
    """

    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
