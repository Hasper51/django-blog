from django.contrib import admin
# Register your models here.
from core.apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'notification_type', 'target_id','target_type', 'created_at')
    readonly_fields = ['id', 'recipient', 'actor', 'notification_type', 'target_id','target_type', 'created_at']