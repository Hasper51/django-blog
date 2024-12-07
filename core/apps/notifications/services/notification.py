from abc import ABC, abstractmethod
from typing import List
from django.db import transaction

from core.apps.notifications.entities import Notification as NotificationEntity
from core.apps.notifications.models import Notification as NotificationModel


class BaseNotificationService(ABC):
    @abstractmethod
    def create_notification(self, notification: NotificationEntity) -> NotificationEntity:
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int) -> None:
        pass

    @abstractmethod
    def get_user_notifications(self, user_id: int) -> List[NotificationEntity]:
        pass


class ORMNotificationService(BaseNotificationService):
    def _to_entity(self, notification: NotificationModel) -> NotificationEntity:
        return NotificationEntity(
            id=notification.id,
            recipient_id=notification.recipient_id,
            actor_id=notification.actor_id,
            notification_type=notification.notification_type,
            target_id=notification.target_id,
            target_type=notification.target_type,
            is_read=notification.is_read,
            created_at=notification.created_at
        )

    def create_notification(self, notification: NotificationEntity) -> NotificationEntity:
        db_notification = NotificationModel.objects.create(
            recipient_id=notification.recipient_id,
            actor_id=notification.actor_id,
            notification_type=notification.notification_type,
            target_id=notification.target_id,
            target_type=notification.target_type,
            is_read=notification.is_read
        )
        return self._to_entity(db_notification)

    def mark_as_read(self, notification_id: int) -> None:
        with transaction.atomic():
            NotificationModel.objects.filter(id=notification_id).update(is_read=True)

    def get_user_notifications(self, user_id: int) -> List[NotificationEntity]:
        notifications = NotificationModel.objects.filter(recipient_id=user_id)
        return [self._to_entity(notification) for notification in notifications]
