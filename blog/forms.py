from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Post, About


class PostMarkDownForm(forms.ModelForm):
    """
    Post模型的body属性为Markdown属性
    """
    body = forms.CharField(widget=AdminPagedownWidget(show_preview=True))  # 提供预览，默认提供

    class Meta:
        fields = "__all__"
        model = Post
