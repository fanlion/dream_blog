from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponse
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from blog.models import Post, Category, Tag
from comments.forms import CommentForm
from blog.forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
import markdown


# @cache_page(60 * 30)  # 缓存30分钟
def index(request, page_size=10):
    """
    主页
    :param request:
    :param page_size: 每页大小，默认为10
    :return:
    """
    post_list = Post.objects.filter(is_pub=True).order_by('-create_time')  # 获取所有发表的文章
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

    #  如果文章是公开，则显示
    if post.is_pub:
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
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
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')

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
    post_list = Post.objects.filter(category=cate).order_by('-create_time')

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
    post_list = Post.objects.filter(tags=t).order_by('-create_time')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})


def contact(request):
    """
    联系我 视图
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_text = {'data': '感谢您的留言，我将尽快与你联系'}
            return JsonResponse(success_text)
        else:
            return render(request, 'blog/contact.html')
    else:
        form = ContactForm()
        return render(request, 'blog/contact.html', context={'form': form})


# @cache_page(60 * 60 * 12)  # 十二小时
def about(request):
    """
    关于我页面 视图
    :param request: 
    :return: 
    """
    return render(request, 'blog/about.html')
