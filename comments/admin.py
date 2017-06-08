from django.contrib import admin
from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    评论管理
    """
    list_display = ['name', 'email', 'url', 'created_time']
    search_fields = ['name']
    list_per_page = 10
