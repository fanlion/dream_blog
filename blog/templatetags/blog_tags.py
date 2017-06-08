from django import template
from django.views.decorators.cache import cache_page

from blog.models import Post, Category, Tag
from comments.models import Comment

register = template.Library()


@cache_page(60 * 30)
@register.simple_tag
def get_recent_posts(num=5):
    """
     自定义标签，用来获取最近发布的文章 
    :param num: 文章数，默认5
    :return: 
    """
    return Post.objects.all().order_by('-create_time')[:num]


@cache_page(60 * 30)
@register.simple_tag
def archives():
    """
    自定义标签，实现按月归档
    :return: 
    """
    return Post.objects.dates('create_time', 'month', order='DESC')


@cache_page(60 * 30)
@register.simple_tag
def get_categories():
    """
    自定义标签,分类模板
    :return: 
    """
    return Category.objects.all()


@cache_page(60 * 30)
@register.simple_tag
def get_tags():
    """
    自定义标签，获取文章标签列表
    :return: 
    """
    return Tag.objects.all()


@cache_page(60 * 30)
@register.simple_tag
def get_recommend_article():
    """
    自定义标签，获取推荐文章列表
    :return: 
    """
    return Post.objects.filter(is_recommend=True).filter(is_pub=True).order_by('-create_time')[:6]


@cache_page(60 * 30)
@register.simple_tag
def get_recent_comments(count=5):
    """
    自定义标签，最近评论
    :return: 
    """
    comments = Comment.objects.order_by('-created_time').distinct()[:count]  # 最近的5条评论
    return comments


@cache_page(60 * 30)
@register.simple_tag
def get_article_by_id(pk):
    return Post.objects.get(pk=pk)


@cache_page(60 * 30)
@register.simple_tag
def get_post_count_by_category(category_id):
    """
    根据category_id获取该分类文章的条数
    :param category_id: 
    :return: 
    """
    return Post.objects.filter(category_id=category_id).count()
