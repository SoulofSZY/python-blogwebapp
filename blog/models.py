# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

    def __str__(self):
        return self.title

    # 用于生成访问url 是否可以换成property
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 在模型中指定排序
    class Meta:
        ordering = ['-created_time']
