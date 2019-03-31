from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post
from .forms import CommentForm


def post_comment(request, post_pk):
    # 1.获取评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # 2.非post请求,直接重定向到文章详情页
    if request.method != 'POST':
        # redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数
        # 如果接收模型实例，那么这个实例必须实现了 get_absolute_url 方法，
        # 这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向
        return redirect(post)

    # 3.处理表单post请求的参数
    # 用户提交的数据存在 request.POST 中，这是一个类字典对象。可用于构造django表单对象
    form = CommentForm(request.POST)
    if form.is_valid():  # Django自动检查表单的数据是否符合格式要求
        # 调用表单的 save 方法保存数据到数据库
        # commit=False的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)
        # 关联评论和文章
        comment.post = post
        # 保存数据
        comment.save()
        # 重定向到文章详情页
        return redirect(post)
    else:
        # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
        # 获取文章的评论列表
        comment_list = post.comment_set.all()
        context = {
            'post': post,
            'form': form,
            'comment_list': comment_list
        }
        return render(request, 'blog/detail.html', context=context)
