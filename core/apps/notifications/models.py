from django.db import models

from core.apps.notifications.entities import Notification as NotificationEntity
from core.apps.users.models import User


# Create your models here.
class NotificationType(models.TextChoices):
    FOLLOW = 'FOLLOW', 'Follow'
    POST = 'POST', 'New Post'
    COMMENT = 'COMMENT', 'New Comment'
    POST_LIKE = 'POST_LIKE', 'New Like'
    COMMENT_LIKE = 'COMMENT_LIKE', 'New Like'


class Notification(models.Model):
    """Represents system notifications for user activities.

    Tracks various types of interactions like likes, comments, and
    follows.

    """

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_received',
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_created',
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
    )
    target_id = models.PositiveIntegerField()
    target_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} by {self.actor.username}"

    def to_entity(self) -> NotificationEntity:
        return NotificationEntity(
            id=self.id,
            recipient_id=self.recipient.id,
            actor_id=self.actor.id,
            notification_type=self.notification_type,
            target_id=self.target_id,
            target_type=self.target_type,
            is_read=self.is_read,
            created_at=self.created_at,
        )
