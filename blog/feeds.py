from django.contrib.syndication.views import Feed
from .models import Post


class AllPostRssFeed(Feed):
    """
    RSS订阅
    """
    title = 'VanBlog博客'
    link = '/'

    description = 'VanBlog博客上的文章'

    def items(self):
        return Post.objects.all().filter(is_pub=True).filter(category__is_pub=True).order_by('-create_time')

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
