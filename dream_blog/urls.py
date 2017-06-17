"""dream_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
import xadmin
from blog.feeds import AllPostRssFeed

urlpatterns = [
    url(r'', include('blog.urls', namespace='blog')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^all/rss/$', AllPostRssFeed(), name='rss'),
    url(r'^search/', include('haystack.urls')),
]

#  给UEditor设置
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
