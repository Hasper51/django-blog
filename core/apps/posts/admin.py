from django.contrib import admin

from core.apps.posts.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('caption', 'author', 'created_at', 'updated_at')

