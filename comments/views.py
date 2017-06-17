from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from comments.models import CommentTest


@csrf_exempt
def neteasy_comment_callback(request):
    data = request.body.decode('utf-8')
    comm = CommentTest(data=data)
    comm.save()
    print(data)
    return HttpResponse()
