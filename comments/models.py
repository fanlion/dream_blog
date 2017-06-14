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

    #
    post = models.ForeignKey('blog.Post', editable=False, verbose_name='文章')  # 被评论的文章
    # title = models.CharField(max_length=200, verbose_name='文章标题')
    # post_url = models.URLField(blank=True, verbose_name='文章地址')
    # post_create_time = models.DateTimeField(verbose_name='文章创建时间')
    # comment_id = models.CharField(max_length=20, verbose_name='评论ID')
    # comment_content = models.TextField(verbose_name='评论内容')
    # comment_pid = models.CharField(max_length=20, verbose_name='父节点')
    # comment_ip = models.CharField(max_length=20, verbose_name='用户IP')
    # comment_source = models.CharField(max_length=10, verbose_name='来源')  # app, web, wap
    # comment_anonymous = models.BooleanField(verbose_name='匿名')  # True 匿名
    # attachment_type = models.CharField(max_length=1, verbose_name='附件类型')  # 0没有附件 1为图片 2为语音 3为视频
    # attachment_desc = models.CharField(max_length=200, verbose_name='附件描述')  # 描述
    # attachment_info = models.CharField(max_length=200, verbose_name='附件地址')  # 附件地址
    # user_id = models.CharField(max_length=100, verbose_name='用户ID')  # 第三方用户ID
    # user_nickname = models.CharField(max_length=100, verbose_name='用户昵称')  # 第三方用户昵称
    # user_avatar = models.URLField(verbose_name='头像地址')  # 用户头像地址

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_time']

    def __str__(self):
        return self.text[:20]


@python_2_unicode_compatible
class CommentTest(models.Model):
    data = models.TextField(verbose_name='测试数据')

    class Meta:
        verbose_name = '测试评论'
        verbose_name_plural = verbose_name
