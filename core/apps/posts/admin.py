from django.contrib import admin

from core.apps.posts.models import Comment, Post


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'user', 'created_at', 'updated_at')
    inlines = (CommentInlineAdmin,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'post', 'user', 'created_at', 'updated_at')
    list_select_related = ('post', 'user')

