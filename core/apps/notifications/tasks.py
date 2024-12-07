from celery import shared_task

from core.apps.notifications.entities import Notification as NotificationEntity
from core.apps.notifications.services.notification import BaseNotificationService
from core.project.containers import get_container


@shared_task
def create_notification_task(
    recipient_id: int,
    actor_id: int,
    notification_type: str,
    target_id: int,
    target_type: str,
):
    container = get_container()
    service = container.resolve(BaseNotificationService)
    notification = NotificationEntity(
        recipient_id=recipient_id,
        actor_id=actor_id,
        notification_type=notification_type,
        target_id=target_id,
        target_type=target_type,
        is_read=False,
    )
    service.create_notification(notification)
