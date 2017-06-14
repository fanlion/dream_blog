from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.db.models import Q

import markdown


# @cache_page(60 * 30)  # 缓存30分钟
def index(request, page_size=15):
    """
    主页
    :param request:
    :param page_size: 每页大小，默认为15
    :return:
    """
    post_list = Post.objects.filter(is_pub=True).filter(tags__is_pub=True).filter(category__is_pub=True).order_by(
        '-create_time')  # 获取所有发表的文章

    paginator = Paginator(post_list, page_size)

    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# @cache_page(60 * 30)
def detail(request, pk):
    """
    文章详情
    :param request: 
    :param pk: 文章id
    :return: 
    """
    post = get_object_or_404(Post, pk=pk)

    # 访问量+1
    post.increase_views()

    # tags = Tag.objects.all(post=post)  # 该文章的所有标签
    # cate = Category.objects.get(post=post)  # 该文章分类
    #
    # is_all_tags_pub = True
    # # 是否所有标签都为公开
    # for t in tags:
    #     if not t.is_pub:
    #         is_all_tags_pub = False

    # TODO 需要判断标签，分类是否为公开
    # 如果文章是公开，则显示
    if post.is_pub:
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        # 评论表单
        form = CommentForm()
        # 获取评论
        comment_list = post.comment_set.all()
        return render(request, 'blog/detail.html', context={'post': post,
                                                            'form': form,
                                                            'toc': md.toc,
                                                            'comment_list': comment_list})
    else:
        raise Http404(' 访问的页面不存在')


# @cache_page(60 * 30)
def archives(request, year, month):
    """
     归档视图，按日期（年，月）对文章进行归档
     该视图查看某日期下的所有文章
    :param request:
    :param year:
    :param month:
    :return:
    """
    post_list = Post.objects.filter(is_pub=True).filter(create_time__year=year, create_time__month=month).order_by(
        '-create_time')

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})


# @cache_page(60 * 30)
def category(request, pk):
    """
    分类视图，查看指定分类的文章
    :param request:
    :param pk: 文章主页
    :return:
    """
    cate = get_object_or_404(Category, pk=pk)
    if cate.is_pub:
        post_list = Post.objects.filter(category=cate).order_by('-create_time')
    else:
        return HttpResponseForbidden('Forbidden 403')

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    """
    返回指定标签下的文章视图
    :param request: 
    :param pk: tag的id
    :return: 
    """
    t = get_object_or_404(Tag, pk=pk)
    if t.is_pub:
        post_list = Post.objects.filter(tags=t).order_by('-create_time')
        paginator = Paginator(post_list, 10)
    else:
        # 无权访问未公开tag下的文章
        return HttpResponseForbidden('Forbidden 403')

    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})


# @cache_page(60 * 60 * 12)  # 十二小时
def about(request):
    """
    关于我页面 视图
    :param request: 
    :return: 
    """
    return render(request, 'blog/about.html')


def search(request, page_size=10):
    """
    全文搜索
    :param request: 
    :param page_size: 
    :return: 
    """
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).filter(is_pub=True).filter(
        tags__is_pub=True).filter(category__is_pub=True).order_by(
        '-create_time')
    paginator = Paginator(post_list, page_size)

    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post_list': post_list})
