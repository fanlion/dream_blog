import xadmin
from .models import Post, Category, Tag, About, FriendSite, VisitRecord, VisitStatistics, BlackList
from xadmin import views

# 管理界面每页展示多少条目
LIST_PER_PAGE = 10


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
        queryset.update(is_pub=True)

    def make_recommend(self, request, queryset):
        queryset.update(is_recommend=True)

    def unmake_published(self, request, queryset):
        queryset.update(is_pub=False)

    def unmake_recommend(self, request, queryset):
        queryset.update(is_recommend=False)

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
    list_filter = ['created_time', 'is_pub']
    list_editable = ('name', 'is_pub')

    def make_published(self, request, queryset):
        queryset.update(is_pub=True)

    def unmake_published(self, request, queryset):
        queryset.update(is_pub=False)

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
        queryset.update(is_pub=True)

    def unmake_published(self, request, queryset):
        queryset.update(is_pub=False)

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
        queryset.update(is_pub=False)

    def make_published(self, request, queryset):
        queryset.update(is_pub=True)

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
        queryset.update(is_pub=False)

    def make_published(self, request, queryset):
        queryset.update(is_pub=True)

    unmake_published.short_description = '取消公开'
    make_published.short_description = '公开'
    actions = [unmake_published, make_published]


class VisitRecordAdmin(object):
    """
    游客访问记录 管理
    """
    list_display = ('ip', 'http_path', 'created_time')
    list_per_page = LIST_PER_PAGE
    search_fields = ['ip']
    model_icon = 'fa fa-file'
    list_filter = ['created_time', 'ip', 'http_path']


class VisitStatisticsAdmin(object):
    """
    运营统计 管理
    """
    list_display = ('created_date', 'today_visit')
    list_per_page = LIST_PER_PAGE
    model_icon = 'fa fa-dashboard'
    list_filter = ['created_date']

    aggregate_fields = {"today_visit": "sum"}

    def _chart_month(self, obj):
        return obj.created_date.strftime('%B')

    data_charts = {
        'today_visit': {
            'title': u'访问量趋势图', 'x-field': 'created_date', 'y-field': ('today_visit',),
            'order': ('created_date',),
        },

        "per_month": {
            'title': u"月访问量", "x-field": "_chart_month", "y-field": ("today_visit",),
            "option": {
                "series": {"bars": {"align": "center", "barWidth": 0.8, 'show': True}},
                "xaxis": {"aggregate": "sum", "mode": "categories"},
            },
        },

    }


class BlackListAdmin(object):
    """
    黑名单管理
    """
    list_display = ('ip', 'created_time', 'is_disable','deny_reason')
    list_per_page = LIST_PER_PAGE
    search_fields = ['ip']
    model_icon = 'fa fa-lock'
    list_filter = ['created_time', 'ip', 'deny_reason', 'is_disable']
    list_editable = ('is_disable', 'deny_reason')

    def unmake_deny(self, request, queryset):
        queryset.update(is_disable=False)

    def make_deny(self, request, queryset):
        queryset.update(is_disable=True)

    unmake_deny.short_description = '解除禁止'
    make_deny.short_description = '禁止访问'
    actions = [unmake_deny, make_deny]

xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(About, AboutAdmin)
xadmin.site.register(FriendSite, FriendSiteAdmin)
xadmin.site.register(VisitRecord, VisitRecordAdmin)
xadmin.site.register(VisitStatistics, VisitStatisticsAdmin)
xadmin.site.register(BlackList, BlackListAdmin)