# from django import template
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Count, Sum
# from blog.models import Post, Category, Tag, FriendSite, VisitStatistics
# from comments.models import Comment
# from django.utils import timezone
#
# register = template.Library()
#
#
# @register.simple_tag
# def get_recent_posts(num=6):
#     """
#      自定义标签，用来获取最近发布的文章
#     :param num: 文章数，默认6
#     :return:
#     """
#     return Post.objects.all().filter(is_pub=True).filter(category__is_pub=True).order_by('-create_time')[:num]
#
#

