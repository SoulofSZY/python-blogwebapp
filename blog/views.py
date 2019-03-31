import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from comment.forms import CommentForm
from .models import Post, Category


def index(request):
    return HttpResponse('欢迎访问我的博客首页！')


# 使用Django模板
def index2(request):
    return render(request, "blog/index_temp.html", context={
        "title": "我的博客首页",
        "welcome": "欢迎访问我的博客首页！"
    })


# 从数据库捞取数据
def index3(request):
    # 在模型中指定了默认排序
    # post_list = Post.objects.all().order_by("created_time")
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={"post_list": post_list})


# 博客文章详情页
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 对Markdown语法的扩展
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',  # 包含很多扩展
        'markdown.extensions.codehilite',  # 语法高亮扩展
        'markdown.extensions.toc',  # 自动生成目录
    ])

    form = CommentForm()
    comment_list = post.comment_set.all()

    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'blog/detail.html', context=context)


# 获取指定归档的文章
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate).order_by('-created_time')
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
