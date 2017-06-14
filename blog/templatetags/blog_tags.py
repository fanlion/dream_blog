from django import template
from django.db.models import Count
from blog.models import Post, Category, Tag
from comments.models import Comment

register = template.Library()


@register.simple_tag
def get_recent_posts(num=6):
    """
     自定义标签，用来获取最近发布的文章 
    :param num: 文章数，默认6
    :return: 
    """
    return Post.objects.all().filter(is_pub=True).order_by('-create_time').filter(is_pub=True)[:num]


@register.simple_tag
def archives():
    """
    自定义标签，实现按月归档
    :return: 
    """
    return Post.objects.filter(is_pub=True).dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """
    自定义标签,分类模板
    :return: 
    """
    return Category.objects.filter(is_pub=True).annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    """
    自定义标签，获取文章标签列表
    :return: 
    """
    # 按post聚集，并指定命名变量num_posts,并且要求只显示数量大于0的标签
    return Tag.objects.filter(is_pub=True).annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_recommend_article():
    """
    自定义标签，获取推荐文章列表
    :return: 
    """
    return Post.objects.filter(is_pub=True).filter(is_recommend=True).filter(is_pub=True).order_by('-create_time')[:6]


@register.simple_tag
def get_recent_comments(num=6):
    """
    自定义标签，最近评论
    :return: 
    """
    comments = Comment.objects.order_by('-created_time').distinct()[:num]  # 最近的num条评论
    return comments


@register.simple_tag
def get_article_by_id(pk):
    """
    根据id获取文章
    :param pk: 
    :return: 
    """
    return Post.objects.filter(is_pub=True).get(pk=pk)
