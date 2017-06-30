from django import forms


class ContactForm(forms.Form):
    """
    联系我表单
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '你的名字'}),
                           max_length=10,
                           error_messages={'required': '名称不能为空', 'max_length': '不超过10字'})
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '留言的主题'}),
                              max_length=100,
                              error_messages={'required': '主题不能为空', 'max_length': '不超过100字'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '你的邮箱'}),
                             error_messages={'required': '邮箱不能为空'})
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '联系内容'}),
                              max_length=400,
                              error_messages={'required': '内容不能为空', 'max_length': '不超过400字'})
    check_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '验证码'}),
                                 error_messages={'required': '验证码不能为空'})
