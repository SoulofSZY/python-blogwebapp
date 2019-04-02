#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename:XX.py
from django.db.models.aggregates import Count
from django import template
from ..models import Post, Category

register = template.Library()


# 最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
    # 获取分类时 统计分类下的文章数 并过滤文章数为0的分类 return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
