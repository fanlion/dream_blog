import xadmin
from .models import Post, Category, Tag, About, FriendSite
from xadmin import views

# 管理界面每页展示多少条目
LIST_PER_PAGE = 15


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True  # 允许选择主题
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    site_title = 'VanBlog 管理'
    site_footer = '李繁的个人博客'
    menu_style = 'default'  # 还有一个'accordion'选项，左侧选项卡是否可以收缩


class PostAdmin(object):
    """
    文章管理
    """
    list_display = ('pk', 'title', 'create_time', 'category', 'is_pub', 'is_recommend', 'views')
    list_display_links = ('pk', 'title')
    list_per_page = LIST_PER_PAGE
    search_fields = ['title']
    model_icon = 'fa fa-laptop'
    list_filter = ['is_pub', 'create_time', 'is_recommend']
    list_editable = ('title', 'is_pub', 'is_recommend', 'views')

    def make_published(self, request, queryset):
        """发布文章Action,用于回调"""
        rows_updated = queryset.update(is_pub=True)
        self.message_user(request, "%s篇文章标记为发布状态." % rows_updated)  # 向用户反馈信息

    def make_recommend(self, request, queryset):
        """推荐文章Action,用于回调"""
        rows_updated = queryset.update(is_recommend=True)
        self.message_user(request, "%s篇文章标记为推荐状态." % rows_updated)  # 向用户反馈信息

    def unmake_published(self, request, queryset):
        """取消发布文章Action"""
        rows_updated = queryset.update(is_pub=False)
        self.message_user(request, "%s篇文章标记为非发布状态." % rows_updated)  # 向用户反馈信息

    def unmake_recommend(self, request, queryset):
        """取消推荐文章Action"""
        rows_updated = queryset.update(is_recommend=False)
        self.message_user(request, "%s篇文章标记为非推荐状态." % rows_updated)  # 向用户反馈信息

    make_published.short_description = '发布'
    make_recommend.short_description = '推荐'
    unmake_published.short_description = '取消发布'
    unmake_recommend.short_description = '取消推荐'

    actions = [make_published, make_recommend, unmake_published, unmake_recommend]


class CategoryAdmin(object):
    """
    分类管理
    """
    list_display = ('name', 'created_time', 'modified_time', 'is_pub')
    list_per_page = LIST_PER_PAGE
    search_fields = ['name']
    model_icon = 'fa fa-sitemap'
    list_filter = ['created_time']
    list_editable = ('name', 'is_pub')

    def make_published(self, request, queryset):
        """分类公开 Action"""
        rows_updated = queryset.update(is_pub=True)
        self.message_user(request, "%s个分类标记为公开状态." % rows_updated)  # 向用户反馈信息

    def unmake_published(self, request, queryset):
        """取消分类公开 Action"""
        rows_updated = queryset.update(is_pub=False)
        self.message_user(request, "%s个分类标记为非公开状态." % rows_updated)  # 向用户反馈信息

    make_published.short_description = '公开'
    unmake_published.short_description = '取消公开'
    actions = [make_published, unmake_published]


class TagAdmin(object):
    """
    文章标签管理
    """
    list_display = ('name', 'created_time', 'modified_time', 'is_pub')
    list_per_page = LIST_PER_PAGE
    search_fields = ['name']
    model_icon = 'fa fa-tag'
    list_filter = ['created_time']
    list_editable = ('name', 'is_pub')

    def make_published(self, request, queryset):
        """分类公开 Action"""
        rows_updated = queryset.update(is_pub=True)
        self.message_user(request, "%s个标签标记为公开状态." % rows_updated)  # 向用户反馈信息

    def unmake_published(self, request, queryset):
        """取消分类公开 Action"""
        rows_updated = queryset.update(is_pub=False)
        self.message_user(request, "%s个标签标记为非公开状态." % rows_updated)  # 向用户反馈信息

    make_published.short_description = '公开'
    unmake_published.short_description = '取消公开'
    actions = [make_published, unmake_published]


class AboutAdmin(object):
    """
    关于我 管理
    """
    list_display = ('title', 'created_time', 'is_pub', 'views')
    list_per_page = LIST_PER_PAGE
    search_fields = ['name']
    model_icon = 'fa fa-leaf'
    list_filter = ['created_time']
    list_editable = ('title', 'is_pub', 'views')

    def unmake_published(self, request, queryset):
        """关于我取消公开 Action"""
        rows_updated = queryset.update(is_pub=False)
        self.message_user(request, "%s篇文章标记为非公开状态." % rows_updated)  # 向用户反馈信息

    def make_published(self, request, queryset):
        """关于我公开 Action"""
        rows_updated = queryset.update(is_pub=True)
        self.message_user(request, "%s篇文章标记为公开状态." % rows_updated)  # 向用户反馈信息

    unmake_published.short_description = '取消公开'
    make_published.short_description = '公开'
    actions = [unmake_published, make_published]


class FriendSiteAdmin(object):
    """
    链接互换(友链) 管理
    """
    list_display = ('site_name', 'site_url', 'created_time', 'is_pub')
    list_per_page = LIST_PER_PAGE
    search_fields = ['site_url']
    model_icon = 'fa fa-link'
    list_filter = ['created_time', 'is_pub']
    list_editable = ('site_url', 'site_name', 'is_pub')

    def unmake_published(self, request, queryset):
        """关于我取消公开 Action"""
        rows_updated = queryset.update(is_pub=False)
        self.message_user(request, "%s个链接记为非公开状态." % rows_updated)  # 向用户反馈信息

    def make_published(self, request, queryset):
        """关于我公开 Action"""
        rows_updated = queryset.update(is_pub=True)
        self.message_user(request, "%s个链接标记为公开状态." % rows_updated)  # 向用户反馈信息

    unmake_published.short_description = '取消公开'
    make_published.short_description = '公开'
    actions = [unmake_published, make_published]


xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(About, AboutAdmin)
xadmin.site.register(FriendSite, FriendSiteAdmin)
