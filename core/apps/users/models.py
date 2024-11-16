from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.apps.users.entities import UserEntity


# Create your models here.
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Adds additional fields for user profile functionality.

    """

    bio = models.TextField(blank=True, verbose_name="Bio")
    profile_image = models.ImageField(upload_to="user_images/", blank=True)
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
        return UserEntity(self.email, self.date_joined)


class Follow(models.Model):
    """Represents the following relationship between users.

    A user can follow multiple users and can be followed by multiple
    users.

    """

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followed',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
