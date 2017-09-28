# @cache_page(60 * 30)  # 缓存30分钟
from django.http import JsonResponse
from .models import Comment


def star(request):
    """
    点赞
    :param request:
    :return:
    """
    return JsonResponse()


def un_star(request):
    """
    踩
    :param request:
    :return:
    """
    return JsonResponse()


def comment(request):
    """
    评论
    :param request:
    :return:
    """
    return JsonResponse()
