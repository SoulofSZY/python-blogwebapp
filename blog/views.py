import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from django.db.models import Q
from comment.forms import CommentForm

from .models import Post, Category, Tag


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


def search(request):
    q = request.GET.get("q")
    error_msg = ''

    if not q:
        error_msg = '请输入关键字！'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {
        'error_msg': error_msg,
        'post_list': post_list,
    })


## 类视图的方式来完成请求处理 代码的进一步抽离 开发只需做基本的业务处理即可

from django.views.generic import ListView, DetailView


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    # 基于类的通用视图已经封装好了分页功能  具体实现 django.core.paginator.Paginator
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # 重写 获取contex的方法 目的：携带自定义分页信息
        context = super(IndexView, self).get_context_data(**kwargs)

        # 获取django paginator 分页信息
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    # 由于django内置的分页 效果比较简单 这里字定义形如 1...2 3 [4] 5 6...10 这样的分页效果
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页则返回{}
            return {}
        # 当前分页左边的页码号
        left = []
        # 当前分页右边的页码号
        right = []
        # 页码1 后是否需要显示省略号
        left_has_more = False
        # 最后页码前是否要显示省略号
        right_has_more = False
        # 是否要显示页码1 当left[] 不包含页码1时显示
        first = False
        # 是否显示最后页码 当right[] 不包含最后页码时显示
        last = False

        # 当前请求的页码号
        page_number = page.number
        # 分页后的总页数
        total_pages = paginator.num_pages
        # 整个分页的页码列表
        page_range = list(paginator.page_range)

        if page_number == 1:
            # 如果当前为第一页，那么left不需要数据
            right = page_range[page_number:page_number + 2]
            # 如果right中最后的页码号比最后一页的页码号-1还小 则需要展示省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            # 如果right中最后的页码号比最后一页的页码号小 则需要展示last
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            # 尾页
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            # 如果left[0] 比2还要大 则需要展示省略号
            if left[0] > 2:
                left_has_more = True
            # 如果left[0] > 1 则需要展示第一页
            if left[0] > 1:
                first = True
        else:
            # 既不是第一页 也不是 尾页
            # print(page_range)
            # print(type(page_number))
            # print(page_number)
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否显示第一页和第一页后的省略号
            print(left)
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }

        return data


class CategoryView(IndexView):
    # 覆写父类中的该方法 完成结果的过滤查询 父类默认查询实体所有
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


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
        # post.body = markdown.markdown(post.body, extensions=[
        #     'markdown.extensions.extra',
        #     'markdown.extensions.codehilite',
        #     'markdown.extensions.toc'
        # ])
        # 实现页面任意地方插入标题  或者在md文件中指定 [TOC] 标识 md渲染时会在标记处插入目录
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc'
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc

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
