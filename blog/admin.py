from django.contrib import admin
from .models import Post, Category, Tag


# 定制 默认后台列表只显示实体的第一个字段 如下操作可定制显示的字段
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


# 将blog应用中的实体 注册到Django内置的后台管理应用admin
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
