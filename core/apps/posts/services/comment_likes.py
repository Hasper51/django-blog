from abc import ABC, abstractmethod

from django.db import IntegrityError

from core.apps.posts.exeptions.comment_like import LikeAlreadyExists, LikeDoesNotExist
from core.apps.posts.models import CommentLike as CommentLikeModel
from core.apps.posts.entities.comment_likes import CommentLike as CommentLikeEntity

class BaseCommentLikeService(ABC):
    @abstractmethod
    def add_like_to_comment(self, comment_id: int, user_id: int) -> CommentLikeEntity: ...
    
    @abstractmethod
    def delete_like_from_comment(self, comment_id: int, user_id: int) -> None: ...

    @abstractmethod
    def get_likes_count(self, comment_id: int) -> int: ...



class ORMCommentLikeService(BaseCommentLikeService):
    def add_like_to_comment(self, comment_id: int, user_id: int) -> CommentLikeEntity:
        try:
            like = CommentLikeModel.objects.create(user_id=user_id, comment_id=comment_id)
            return like
        except IntegrityError:
            raise LikeAlreadyExists(comment_id=comment_id, user_id=user_id)
    
    def delete_like_from_comment(self, comment_id: int, user_id: int) -> None:
        deleted, _ = CommentLikeModel.objects.filter(comment_id=comment_id, user_id=user_id).delete()
        if deleted == 0:
            raise LikeDoesNotExist(comment_id=comment_id, user_id=user_id)
    
    def get_likes_count(self, comment_id: int) -> int:
        return CommentLikeModel.objects.filter(comment_id=comment_id).count()
