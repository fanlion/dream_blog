import xadmin
from .models import Comment

LIST_PER_PAGE = 10


class CommentAdmin(object):
    """
    评论管理
    """
    list_display = ('nick_name', 'email', 'home_url', 'created_time')
    search_fields = ['nick_name', 'email']
    list_per_page = LIST_PER_PAGE
    list_filter = ['nick_name', 'email', 'created_time']
    model_icon = 'fa fa-comment'


xadmin.site.register(Comment, CommentAdmin)
