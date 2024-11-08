#core\apps\posts\models.py
from django.db import models

from core.apps.common.models import TimeBaseModel
from core.apps.users.models import User
from core.apps.posts.entities.posts import Post as PostEntity

class Post(TimeBaseModel):
    """
    Model extending from TimeBaseModel, that adds the "created_at","updated_at" fields

    Represents a user's post in the platform.
    Users can create posts with images and captions.
    Posts can be liked and commented on by other users.
    """
    image = models.ImageField(upload_to="posts/", blank=True)
    caption = models.TextField(max_length=1000, blank=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author} at {self.created_at}"

    def to_entity(self) -> PostEntity:
        return PostEntity(
            id=self.id,
            image=self.image.url,
            caption=self.caption,
            author=self.author.username,
            created_at=self.created_at,
            updated_at=self.updated_at,
            
        )
    
    def get_likes_count(self):
        return self.post_likes.count()

    def get_comments_count(self):
        return self.comments.count()

class Comment(TimeBaseModel):
    """
    Represents comments on posts.
    Users can comment on posts and these comments can be liked by other users.
    """
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

    def get_likes_count(self):
        return self.comment_likes.count()
    
class PostLike(models.Model):
    """
    Represents likes on posts.
    Users can like posts, with each user only able to like a post once.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post Like'
        verbose_name_plural = 'Post Likes'
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"

class CommentLike(models.Model):
    """
    Represents likes on comments.
    Users can like comments, with each user only able to like a comment once.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment Like'
        verbose_name_plural = 'Comment Likes'
        unique_together = ('user', 'comment')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"