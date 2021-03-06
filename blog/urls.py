from django.conf.urls import url
from blog import views

# app_name = 'blog'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^preview/(?P<pk>[0-9]+)/$', views.preview, name='preview'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag'),
    url(r'^about/$', views.about, name='about'),
    url(r'^preview_about/$', views.preview_about, name='preview_about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'check_code', views.check_code, name='check_code'),
]
