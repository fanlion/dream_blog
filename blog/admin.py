from django.contrib import admin

from blog.forms import MarkDownForm
from blog.models import Post, Category, Tag, Contact


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    文章管理
    """
    form = MarkDownForm

    list_display = ['title', 'create_time', 'modified_time', 'category', 'is_pub', 'is_recommend']
    fields = ['title', 'author', 'views', ('is_pub', 'is_recommend'), 'category', 'tags', 'excerpt', 'body']
    search_fields = ['title']
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    分类管理
    """
    list_display = ['name', 'created_time', 'modified_time']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签管理
    """
    list_display = ['name', 'created_time', 'modified_time']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    留言管理
    """
    list_display = ['name', 'subject', 'created_time']

    search_fields = ['name']
    list_per_page = 10
