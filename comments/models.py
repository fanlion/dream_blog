from django.db import models
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Comment(models.Model):
    """
    评论model
    """
    nick_name = models.CharField(max_length=100, verbose_name='昵称')  # 姓名
    email = models.EmailField(max_length=255, verbose_name='邮箱')  # 邮箱
    home_url = models.URLField(blank=True, verbose_name='个人主页')  # 个人主页地址
    content = models.TextField(verbose_name='评论内容')  # 评论内容
    post = models.ForeignKey('blog.Post', editable=False, verbose_name='文章')  # 被评论的文章
    pid = models.ManyToManyField('self', verbose_name='父节点')  # 父节点
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='修改日期')  # 修改时间

    is_pub = models.BooleanField(default=True, verbose_name='是否显示')  # 是否显示
    star = models.PositiveIntegerField(default=0, verbose_name='赞')  # 赞
    un_star = models.PositiveIntegerField(default=0, verbose_name='踩')  # 踩
    reply_to = models.ManyToManyField('self', verbose_name='回复')  # 回复给

    # title = models.CharField(max_length=200, verbose_name='文章标题')
    # post_url = models.URLField(blank=True, verbose_name='文章地址')
    # comment_pid = models.CharField(max_length=20, verbose_name='父节点')
    # comment_ip = models.CharField(max_length=20, verbose_name='用户IP')
    # comment_source = models.CharField(max_length=10, verbose_name='来源')  # app, web, wap
    # user_avatar = models.URLField(verbose_name='头像地址')  # 用户头像地址

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_time']

    def __str__(self):
        return self.text[:20]
