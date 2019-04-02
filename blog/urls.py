#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename:XX.py

from django.conf.urls import url
from . import views

app_name = 'blog'
# path 视图函数 函数别名
urlpatterns = [
    # url(r"^$", views.index3, name='index'),
    url(r"^$", views.IndexView.as_view(), name='index'),
    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category')
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category')
]
