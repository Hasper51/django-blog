from django.contrib import admin

from core.apps.users.models import (
    Following,
    User,
)


class FollowingInline(admin.TabularInline):
    model = Following
    fk_name = 'follower'
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = [FollowingInline]


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')
    search_fields = ('user', 'follower', 'following')
    