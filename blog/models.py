# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags

import markdown


class Category(models.Model):
    """
        博客分类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
        博客标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
        博客
    """
    # 文章标题
    title = models.CharField(max_length=70)
    # 正文
    body = models.TextField()
    # 创建时间和最后一次修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 摘要 允许为空
    excerpt = models.CharField(max_length=200, blank=True)
    # 外键 分类 n:1
    category = models.ForeignKey(Category)
    # n:n关联 标签
    tags = models.ManyToManyField(Tag, blank=True)

    # 外键 作者 采用Django内置的django.contrib.auth应用
    # django.contrib.auth用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型
    author = models.ForeignKey(User)

    # 粗略统计阅读量 即每次访问详情页阅读量+1
    pviews = models.PositiveIntegerField(default=0)

    def increase_pviews(self):
        self.pviews += 1
        self.save(update_fields=['pviews'])

    def __str__(self):
        return self.title

    # 用于生成访问url 是否可以换成property
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 重写save方法 截取正文的前54个字符作为摘要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            # 不够完美 比如54个字符 最后是html标签的一部分 strip_tags 不会识别出来
            self.excerpt = strip_tags(md.convert(self.body)[:54])
        super(Post, self).save(*args, **kwargs)

    # 在模型中指定排序
    class Meta:
        ordering = ['-created_time']
