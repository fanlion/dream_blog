from django.conf.urls import url
from . import views

# app_name = 'comments'

urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
    url(r'^login', views.github_login_callback, name='github_login'),
    url(r'^callback', views.neteasy_comment_callback, name='callback'),
]
