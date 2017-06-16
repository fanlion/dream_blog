from django.db import models
from users.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
from ckeditor_uploader.fields import RichTextUploadingField


@python_2_unicode_compatible
class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=60, verbose_name='分类')  # 分类名称
    is_pub = models.BooleanField(default=True, verbose_name='是否公开')  # 是否公开

    created_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='创建日期')  # 创建日期
    modified_time = models.DateTimeField(auto_now=True, editable=True, null=True, verbose_name='修改日期')  # 修改日期

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']  # 按哪个排序

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=100, verbose_name='标签')  # 标签名称
    is_pub = models.BooleanField(default=True, verbose_name='是否公开')  # 是否公开

    created_time = models.DateTimeField(verbose_name='创建日期')  # 创建日期
    modified_time = models.DateTimeField(verbose_name='修改日期')  # 修改日期

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']  # 按哪个排序

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=70, verbose_name='标题')  # 标题
    body = RichTextUploadingField(config_name='default', verbose_name='正文')  # ckeditor,配置在工程settings中
    create_time = models.DateTimeField(verbose_name='发布日期')  # 发布时间
    modified_time = models.DateTimeField(verbose_name='修改日期')  # 修改时间
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='摘要')  # 摘要
    is_pub = models.BooleanField(default=True, verbose_name='是否公开')  # 是否公开
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')  # 是否推荐
    is_original = models.BooleanField(default=True, verbose_name='是否原创')  # 是否原创
    category = models.ForeignKey(Category, verbose_name='分类')  # 分类
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')  # 标签
    author = models.ForeignKey(User, verbose_name='作者')  # 作者
    views = models.PositiveIntegerField(default=0, verbose_name='访问量')  # 点击量

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
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
            self.excerpt = strip_tags(self.body)[:74]
        super(Post, self).save(*args, **kwargs)


@python_2_unicode_compatible
class About(models.Model):
    """
    关于 model
    """
    title = models.CharField(max_length=200, verbose_name='标题')  # 标题
    created_time = models.DateTimeField(verbose_name='发布日期')  # 发布时间
    body = RichTextUploadingField(config_name='default', verbose_name='正文')  # ckeditor,配置在工程settings中
    modified_time = models.DateTimeField(verbose_name='修改日期')  # 修改时间
    is_pub = models.BooleanField(default=True, verbose_name='是否公开')  # 是否公开
    views = models.PositiveIntegerField(default=0, verbose_name='访问量')  # 点击量

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = verbose_name

    def increase_views(self):
        """
        更新访问量
        :return: 
        """
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class FriendSite(models.Model):
    """
    友情链接，链接互换
    """
    site_name = models.CharField(max_length=20, blank=False, verbose_name='站点名称')  # 站点名称
    site_url = models.URLField(max_length=150, blank=False, verbose_name='站点地址')  # 站点地址
    admin_name = models.CharField(max_length=30, verbose_name='站长名称')  # 站长名称
    admin_contact = models.CharField(max_length=200, verbose_name='站长联系方式')  # 站长联系方式
    created_time = models.DateTimeField(verbose_name='创建时间')  # 创建时间
    modified_time = models.DateTimeField(verbose_name='修改时间')  # 修改时间
    is_pub = models.BooleanField(default=False, verbose_name='是否发布')  # 默认不发布

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class VisitRecord(models.Model):
    """
    游客访问记录 
    """
    http_host = models.CharField(max_length=30, verbose_name='host')  # HTTP_HOST
    http_path = models.CharField(max_length=40, verbose_name='path')  # 访问链接
    http_user_agent = models.CharField(max_length=350, verbose_name='agent')  # 客户端的user-agent字符串
    ip = models.CharField(max_length=20, verbose_name='ip')  # 客户端的IP地址
    server_name = models.CharField(max_length=10, verbose_name='server_name')  # 服务器的主机名
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='请求时间')  # 访问时间

    class Meta:
        verbose_name = '访问记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


@python_2_unicode_compatible
class VisitStatistics(models.Model):
    """
     站点运营统计数据，每天的有效访问量，访问ip等 
    """
    today_visit = models.PositiveIntegerField(default=0, verbose_name='今日访问量')  # 今日访问量

    created_date = models.DateField(unique=True, editable=True, verbose_name='日期')  # 日期

    class Meta:
        verbose_name = '运营统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.created_date.year) + '年' + str(self.created_date.month) + '月' + str(
            self.created_date.month) + '日'
