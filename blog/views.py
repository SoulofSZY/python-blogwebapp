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

    # 阅读量 + 1
    post.increase_pviews()
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


## 类视图的方式来完成请求处理 代码的进一步抽离 开发只需做基本的业务处理即可

from django.views.generic import ListView, DetailView


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    # 基于类的通用视图已经封装好了分页功能  具体实现 django.core.paginator.Paginator
    paginate_by = 2


class CategoryView(IndexView):
    # 覆写父类中的该方法 完成结果的过滤查询 父类默认查询实体所有
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


# 使用Django 基于详情页的类模板
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 重写get方法的目的是针对 文章阅读量功能
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_pviews()

        return response

    def get_object(self, queryset=None):
        # 重写该方法是为了对post.body进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])

        return post

    def get_context_data(self, **kwargs):
        # 重写该方法 是由于处理指定实体外 还需要传递其他数据到页面
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
