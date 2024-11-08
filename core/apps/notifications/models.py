from django.db import models

from posts.models import (
    Comment,
    Post,
)
from users.models import User


# Create your models here.


class Notification(models.Model):
    """Represents system notifications for user activities.

    Tracks various types of interactions like likes, comments, and
    follows.

    """

    NOTIFICATION_TYPES = (
        ('like_post', 'Like Post'),
        ('like_comment', 'Like Comment'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications',
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='acted_notifications',
    )
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} by {self.actor.username}"
