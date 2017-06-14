import json

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from .forms import CommentForm
from comments.models import CommentTest
from comments import settings as blog_settings


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 根据request生成表单
        form = CommentForm(request.POST)

        # 校验表单数据
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)

    return redirect(post)


@csrf_exempt
def neteasy_comment_callback(request):
    data = request.body.decode('utf-8')
    comm = CommentTest(data=data)
    comm.save()
    print(data)
    return HttpResponse()


def github_login_callback(request):
    """
    github游客登录
    :param request: 
    :return: 
    """
    code = request.GET.get('code')  # 获取GitHub返回的code
    access_token_url = 'https://github.com/login/oauth/access_token'

    # 从配置文件中读取配置信息
    client_id = blog_settings.GITHUB_CLIENT_ID
    client_secret = blog_settings.GITHUB_CLIENT_SECRET
    redirect_url = blog_settings.GITHUB_REDIRECT_URL

    # 配置请求参数
    access_token_params = {'code': code,
                           'client_id': client_id,
                           'client_secret': client_secret,
                           'redirect_url': redirect_url}

    access_token_data = requests.get(url=access_token_url, params=access_token_params).text

    # 获取到access_token
    access_token = access_token_data.split('&')[0].split('=')

    user_data_url = 'https://api.github.com/user?access_token=xxx'
    user_data_params = {'access_token': access_token}

    user_data = requests.get(url=user_data_url, params=user_data_params).json()

    return JsonResponse(user_data)
