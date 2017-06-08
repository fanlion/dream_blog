from django import forms
from .models import Contact
from pagedown.widgets import AdminPagedownWidget
from .models import Post


class ContactForm(forms.ModelForm):
    """
    联系我  表单
    """

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']


class MarkDownForm(forms.ModelForm):
    """
    Post模型的body属性为Markdown属性
    """
    body = forms.CharField(widget=AdminPagedownWidget(show_preview=True))  # 提供预览，默认提供

    class Meta:
        fields = "__all__"
        model = Post
