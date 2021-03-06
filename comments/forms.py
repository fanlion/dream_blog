from django import forms


class CommentForm(forms.Form):
    """
    联系我表单
    """
    nick_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '你的名字'}),
                                max_length=10,
                                error_messages={'required': '名称不能为空', 'max_length': '不超过10字'})
    home_url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': '个人主页'}),
                              max_length=100,
                              error_messages={'max_length': '不超过100字'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '你的邮箱'}),
                             error_messages={'required': '邮箱不能为空'})
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '评论内容'}),
                              max_length=400,
                              error_messages={'required': '内容不能为空', 'max_length': '不超过400字'})
    check_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '验证码'}),
                                 error_messages={'required': '验证码不能为空'})
