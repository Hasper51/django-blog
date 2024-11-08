from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser. Adds additional
    fields for user profile functionality.

    Inherits default fields: username, email, password, first_name, last_name, is_active, etc.

    """

    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="user_images/", blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_followers_count(self):
        return self.followed.count()

    def get_following_count(self):
        return self.follower.count()


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
