from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from blog.forms import ContactForm
from .models import Post, Category, Tag, About, Contact
from comments.models import Comment
from .utils.page_helper import PaginationBlogPost

PAGE_SIZE = 12  # 每页显示文章的数量


# @cache_page(60 * 30)  # 缓存30分钟
def index(request):
    """
    主页
    :param request:
    :return:
    """
    post_list = Post.objects.filter(is_pub=True).filter(category__is_pub=True).order_by(
        '-create_time')  # 获取所有发表的文章
    page = request.GET.get('page')

    is_paginated = False
    if post_list.count() > PAGE_SIZE:
        is_paginated = True

    paginator = Paginator(post_list, PAGE_SIZE)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第一页
        page_obj = paginator.page(1)
    except EmptyPage:
        # 如果page超出了总页数，返回最后一页
        page_obj = paginator.page(paginator.num_pages)

    # pagination_data是一个包含分页信息的字典
    pagination_data = PaginationBlogPost(paginator=paginator,
                                         page_obj=page_obj, is_paginated=is_paginated).pagination_data()

    pagination_data['post_list'] = page_obj
    pagination_data['page_obj'] = page_obj
    pagination_data['paginator'] = paginator

    return render(request, 'blog/index.html', pagination_data)


# @cache_page(60 * 30)
def detail(request, pk):
    """
    文章详情
    :param request: 
    :param pk: 文章id
    :return: 
    """
    post = get_object_or_404(Post, pk=pk)
    cate = get_object_or_404(Category, post=post)
    comments = Comment.objects.filter(post=post).filter(is_pub=True)

    # 访问量+1
    post.increase_views()

    # 如果文章是公开，则显示
    if post.is_pub and cate.is_pub:
        # 获取评论
        return render(request, 'blog/detail.html', {'post': post, 'comments': comments})
    else:
        raise Http404('访问的页面不存在')


@login_required
def preview(request, pk):
    """
    文章详情
    :param request: 
    :param pk: 文章id
    :return: 
    """
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/detail.html', {'post': post})  # @cache_page(60 * 30)


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
    post_list = Post.objects.filter(
        is_pub=True).filter(
        category__is_pub=True).filter(
        create_time__year=year,
        create_time__month=month).order_by(
        '-create_time')

    page = request.GET.get('page')
    is_paginated = False
    if post_list.count() > PAGE_SIZE:
        is_paginated = True

    paginator = Paginator(post_list, PAGE_SIZE)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第一页
        page_obj = paginator.page(1)
    except EmptyPage:
        # 如果page超出了总页数，返回最后一页
        page_obj = paginator.page(paginator.num_pages)

    # pagination_data是一个包含分页信息的字典
    pagination_data = PaginationBlogPost(paginator=paginator, page_obj=page_obj,
                                         is_paginated=is_paginated).pagination_data()

    pagination_data['post_list'] = page_obj
    pagination_data['page_obj'] = page_obj
    pagination_data['paginator'] = paginator

    return render(request, 'blog/index.html', pagination_data)


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
        post_list = Post.objects.filter(category=cate).filter(is_pub=True).order_by('-create_time')
    else:
        raise Http404('访问的页面不存在')

    page = request.GET.get('page')

    is_paginated = False
    if post_list.count() > PAGE_SIZE:
        is_paginated = True

    paginator = Paginator(post_list, PAGE_SIZE)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第一页
        page_obj = paginator.page(1)
    except EmptyPage:
        # 如果page超出了总页数，返回最后一页
        page_obj = paginator.page(paginator.num_pages)

    # pagination_data是一个包含分页信息的字典
    pagination_data = PaginationBlogPost(paginator=paginator, page_obj=page_obj,
                                         is_paginated=is_paginated).pagination_data()

    pagination_data['post_list'] = page_obj
    pagination_data['page_obj'] = page_obj
    pagination_data['paginator'] = paginator

    return render(request, 'blog/index.html', pagination_data)


# @cache_page(60 * 30)
def tag(request, pk):
    """
    返回指定标签下的文章视图
    :param request: 
    :param pk: tag的id
    :return: 
    """
    t = get_object_or_404(Tag, pk=pk)
    if t.is_pub:
        post_list = Post.objects.filter(tags=t).filter(is_pub=True).filter(category__is_pub=True).order_by(
            '-create_time')

        page = request.GET.get('page')
        is_paginated = False
        if post_list.count() > PAGE_SIZE:
            is_paginated = True

        paginator = Paginator(post_list, PAGE_SIZE)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # 如果page不是整数，返回第一页
            page_obj = paginator.page(1)
        except EmptyPage:
            # 如果page超出了总页数，返回最后一页
            page_obj = paginator.page(paginator.num_pages)

        # pagination_data是一个包含分页信息的字典
        pagination_data = PaginationBlogPost(paginator=paginator, page_obj=page_obj,
                                             is_paginated=is_paginated).pagination_data()

        pagination_data['post_list'] = page_obj
        pagination_data['page_obj'] = page_obj
        pagination_data['paginator'] = paginator

        return render(request, 'blog/index.html', pagination_data)
    else:
        # 无权访问未公开tag下的文章
        return HttpResponseForbidden('Forbidden 403')


# @cache_page(60 * 60)  # 十二小时
def about(request):
    """
    关于我页面 视图
    :param request: 
    :return: 
    """
    post = About.objects.filter(is_pub=True).order_by('created_time')  # 只能有一篇文章为发布状态
    # 如果有多篇文章
    if post and len(post) >= 1:
        post = post[0]
        post.increase_views()
    return render(request, 'blog/about.html', {'post': post})


def contact(request):
    """
    留言视图
    :param request: 
    :return: 
    """
    # 表单提交时
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            verify_code = form.cleaned_data['check_code']  # 表单中的验证码

            correct_code = request.session.get('CheckCode', None)

            if correct_code and verify_code.upper() == correct_code.upper():
                cont = Contact(name=name, email=email, subject=subject, content=content)
                cont.save()
                result = {'result': '我已经收到你的消息了，我会尽快查看消息！'}
                return JsonResponse(result)
            else:
                result = {'result': '验证码错误, 请重新填写!'}
                return JsonResponse(result)
        else:
            return JsonResponse({'result': '服务器异常，请稍后重试'})
    # get请求页面时
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    import io
    from blog.utils import check_code

    stream = io.BytesIO()
    # img图片对象，code在图像中写的内容
    img, code = check_code.create_validate_code()
    img.save(stream, 'png')
    # 图片页面中显示，验证码存入session
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


# @login_required
def preview_about(request):
    """
    关于我 预览 视图,只允许管理员查看
    :param request:
    :return:
    """
    post = About.objects.order_by('created_time')  # 只能有一篇文章发布
    # 如果有多篇文章
    if post and len(post) >= 1:
        post = post[0]
    return render(request, 'blog/about.html', {'post': post})


def search(request):
    """
    全文搜索
    目前弃用 2017年6月17日16:11:15
    :param request:
    :return:
    """
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).filter(is_pub=True).filter(
        category__is_pub=True).order_by(
        '-create_time')
    return render(request, 'blog/index.html', {'post_list': post_list, 'error_msg': error_msg})
