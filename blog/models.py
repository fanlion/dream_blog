import markdown
from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags


@python_2_unicode_compatible
class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=60, verbose_name='分类')  # 分类名称

    created_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='创建日期')  # 创建日期
    modified_time = models.DateTimeField(auto_now=True, null=True, verbose_name='修改日期')  # 修改日期

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['-created_time']  # 按哪个排序

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=100, verbose_name='标签')  # 标签名称

    created_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='创建日期')  # 创建日期
    modified_time = models.DateTimeField(auto_now=True, null=True, verbose_name='修改日期')  # 修改日期

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['-created_time']  # 按哪个排序

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=70, verbose_name='标题')  # 标题
    body = models.TextField(verbose_name='正文')  # 正文
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='发布日期')  # 发布时间
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改日期')  # 修改时间
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='摘要')  # 摘要
    is_pub = models.BooleanField(default=True, verbose_name='是否公开')  # 是否公开
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')  # 是否推荐
    category = models.ForeignKey(Category, verbose_name='分类')  # 分类
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')  # 标签
    author = models.ForeignKey(User, verbose_name='作者')  # 作者
    views = models.PositiveIntegerField(default=0, verbose_name='访问量')  # 点击量

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-create_time']  # 按哪个排序

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        对象对应的URL
        :return: 
        """
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        """
        更新访问量
        :return: 
        """
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果摘要没有填写，则自动生成
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)


class Contact(models.Model):
    """
    联系内容
    """
    name = models.CharField(max_length=100, verbose_name='联系人')
    email = models.EmailField(max_length=255, verbose_name='邮箱')
    subject = models.CharField(max_length=255, verbose_name='主题')
    message = models.TextField(verbose_name='内容')
    is_pub = models.BooleanField(default=False, verbose_name='是否公开')  # 不公开则不显示在前端页面

    created_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='创建日期')  # 创建日期
    modified_time = models.DateTimeField(auto_now=True, null=True, verbose_name='修改日期')  # 修改日期

    class Meta:
        verbose_name = '游客留言'
        verbose_name_plural = '游客留言'
        ordering = ['-created_time']  # 按哪个排序

    def __str__(self):
        return self.message[:20]
