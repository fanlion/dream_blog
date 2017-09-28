from django.conf.urls import url
from . import views

# app_name = 'comments'

urlpatterns = [
    # url(r'^callback', views.neteasy_comment_callback, name='callback'),
    url(r'^star/(?P<pk>[0-9]+)/$', views.star, name='star'),
    url(r'^un_star/(?P<pk>[0-9]+)/$', views.un_star, name='un_star'),
]
