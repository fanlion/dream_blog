from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    在django的用户模型上扩展自定义User
    """
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')  # 昵称，GitHub的用户名
    url = models.URLField(max_length=255, blank=True, verbose_name='个人主页')  # 个人主页
    photo = models.URLField(max_length=255, blank=True, verbose_name='头像')  # 头像

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        verbose_name_plural = '用户'
