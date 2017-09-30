from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Comment
from .forms import CommentForm
from django.views.decorators.csrf import csrf_exempt


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


@csrf_exempt
def comment(request):
    """
    评论
    :param request:
    :return:
    """
    if request.method == 'POST':
        nick_name = request.POST.get('nick_name')
        email = request.POST.get('email')
        home_url = request.POST.get('home_url')
        content = request.POST.get('content')
        verify_code = request.POST.get('verify_code')
        post_id = request.POST.get('post_id')
        comment_ip = str(request.META.get('REMOTE_ADDR'))
        comment_source = request.META.get('HTTP_USER_AGENT')

        if comment_source:
            # 截取到第一个右括号之前的内容
            comment_source = comment_source[0: comment_source.index(')') + 1]

        correct_code = request.session.get('CheckCode', None)

        if correct_code and verify_code.upper() == correct_code.upper():
            comment_db = Comment()
            comment_db.nick_name = nick_name
            comment_db.email = email
            comment_db.home_url = home_url
            comment_db.content = content
            comment_db.post_id = post_id
            comment_db.comment_ip = comment_ip
            comment_db.comment_source = comment_source
            comment_db.save()
            result = {'result': '你已成功发表伟大的言论'}
            return JsonResponse(result)
        else:
            result = {'result': '验证码错误，请重新填写!'}
            return JsonResponse(result)
    else:
        return HttpResponseNotAllowed('POST')


