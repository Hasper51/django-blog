from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.apps.users.entities import (
    Following as FollowingEntity,
    User as UserEntity,
)


# Create your models here.
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Adds additional fields for user profile functionality.

    """
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, verbose_name="Bio")
    profile_image = models.ImageField(upload_to="user_images/", blank=True, null=True)
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='User Token',
        default=uuid4,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def to_entity(self) -> UserEntity:
        return UserEntity(id=self.pk, email=self.email, date_joined=self.date_joined)


class Following(models.Model):
    """Represents the following relationship between users.

    A user can follow multiple users and can be following by multiple
    users.

    """

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def to_entity(self) -> FollowingEntity:
        return Following(
            id=self.id,
            follower_id=self.follower.id,
            following_id=self.following.id,
            created_at=self.created_at,
        )
