from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    """
    用户注册表单
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
