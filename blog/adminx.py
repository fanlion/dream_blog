import xadmin
from .models import Post, Category, Tag, About
from xadmin import views
from .forms import PostMarkDownForm, AboutMarkDownForm


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

    form = PostMarkDownForm

    list_display = ('title', 'create_time', 'category', 'is_pub', 'is_recommend', 'views')
    list_per_page = 10
    search_fields = ['title']
    model_icon = 'fa fa-laptop'
    list_filter = ['is_pub', 'create_time', 'is_recommend']


class CategoryAdmin(object):
    """
    分类管理
    """
    list_display = ('name', 'created_time', 'modified_time', 'is_pub')
    list_per_page = 10
    search_fields = ['name']
    model_icon = 'fa fa-sitemap'
    list_filter = ['created_time']


class TagAdmin(object):
    """
    文章标签管理
    """
    list_display = ('name', 'created_time', 'modified_time', 'is_pub')
    list_per_page = 10
    search_fields = ['name']
    model_icon = 'fa fa-tag'
    list_filter = ['created_time']


class AboutAdmin(object):
    """
    关于我 管理
    """
    form = AboutMarkDownForm
    list_display = ('title', 'created_time', 'is_pub', 'views')
    list_per_page = 10
    search_fields = ['name']
    model_icon = 'fa fa-leaf'
    list_filter = ['created_time']


xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(About, AboutAdmin)
