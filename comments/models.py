from django.db import models
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Comment(models.Model):
    """
    评论model
    """
    name = models.CharField(max_length=100, verbose_name='名称')  # 姓名
    email = models.EmailField(max_length=255, verbose_name='邮箱')  # 邮箱
    url = models.URLField(blank=True, verbose_name='个人主页')  # 个人主页地址
    text = models.TextField(verbose_name='评论内容')  # 评论内容
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    post = models.ForeignKey('blog.Post', editable=False, verbose_name='文章')  # 被评论的文章

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_time']

    def __str__(self):
        return self.text[:20]


# @python_2_unicode_compatible
# class User(models.Model):
#     """
#     评论时的用户
#     """
#     name = models.CharField(max_length=30, verbose_name='名称')  # 姓名
#     email = models.EmailField(max_length=255, verbose_name='邮箱')  # 邮箱

