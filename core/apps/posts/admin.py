from django.contrib import admin

from core.apps.posts.models import (
    Comment,
    Post,
    PostLike,
)


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 0


class PostLikeInlineAdmin(admin.TabularInline):
    model = PostLike
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'user', 'created_at', 'updated_at')
    inlines = (CommentInlineAdmin, PostLikeInlineAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'post', 'user', 'created_at', 'updated_at')
    list_select_related = ('post', 'user')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_select_related = ('post', 'user')
