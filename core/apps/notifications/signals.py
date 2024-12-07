from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.notifications.models import NotificationType
from core.apps.notifications.tasks import create_notification_task
from core.apps.posts.models import (
    Comment,
    CommentLike,
    Post,
    PostLike,
)
from core.apps.users.models import Following


@receiver(post_save, sender=Following)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        create_notification_task.delay(
            recipient_id=instance.following.id,
            actor_id=instance.follower.id,
            notification_type=NotificationType.FOLLOW,
            target_id=instance.id,
            target_type='Following',
        )


@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    if created:
        for follower in instance.user.followers.all():
            create_notification_task.delay(
                recipient_id=follower.follower.id,
                actor_id=instance.user.id,
                notification_type=NotificationType.POST,
                target_id=instance.id,
                target_type='Post',
            )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        create_notification_task.delay(
            recipient_id=instance.post.user.id,
            actor_id=instance.user.id,
            notification_type=NotificationType.COMMENT,
            target_id=instance.id,
            target_type='Comment',
        )


@receiver(post_save, sender=PostLike)
def create_post_like_notification(sender, instance, created, **kwargs):
    if created:
        create_notification_task.delay(
            recipient_id=instance.post.user.id,
            actor_id=instance.user.id,
            notification_type=NotificationType.POST_LIKE,
            target_id=instance.id,
            target_type='PostLike',
        )


@receiver(post_save, sender=CommentLike)
def create_comment_like_notification(sender, instance, created, **kwargs):
    if created:
        create_notification_task.delay(
            recipient_id=instance.comment.user.id,
            actor_id=instance.user.id,
            notification_type=NotificationType.COMMENT_LIKE,
            target_id=instance.id,
            target_type='CommentLike',
        )
