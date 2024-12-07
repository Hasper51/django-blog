from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.notifications'

    def ready(self):
        try:
            import core.apps.notifications.signals  # Важно импортировать сигналы
        except ImportError:
            pass
    