#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename:XX.py
from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    '''
        RSS  xml格式
    '''

    # 显示聚合阅读器上的标题
    title = '博客教程'
    # 通过聚合阅读器跳转到网站的地址
    link = '/'
    # 显示在聚合阅读器上的描述信息
    description = '这是一个Django教程'

    # 需要展示的文章条目
    def items(self):
        return Post.objects.all()

    # 聚合阅读器中显示条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合阅读器条目内容
    def item_description(self, item):
        return item.body
