from abc import ABC, abstractmethod

from django.db import IntegrityError

from core.apps.posts.exeptions.post_like import LikeAlreadyExists, LikeDoesNotExist
from core.apps.posts.models import PostLike as PostLikeModel
from core.apps.posts.entities.post_likes import PostLike as PostLikeEntity

class BasePostLikeService(ABC):
    @abstractmethod
    def add_like_to_post(self, post_id: int, user_id: int) -> PostLikeEntity: ...
    
    @abstractmethod
    def delete_like_from_post(self, post_id: int, user_id: int) -> None: ...

    @abstractmethod
    def get_likes_count(self, post_id: int) -> int: ...

    @abstractmethod
    def get_users_who_liked_post(self, post_id: int) -> list[int]: ...


class ORMPostLikeService(BasePostLikeService):
    def add_like_to_post(self, post_id: int, user_id: int) -> PostLikeEntity:
        try:
            like = PostLikeModel.objects.create(user_id=user_id, post_id=post_id)
            return like
        except IntegrityError:
            raise LikeAlreadyExists(post_id=post_id, user_id=user_id)
    
    def delete_like_from_post(self, post_id: int, user_id: int) -> None:
        deleted, _ = PostLikeModel.objects.filter(post_id=post_id, user_id=user_id).delete()
        if deleted == 0:
            raise LikeDoesNotExist(post_id=post_id, user_id=user_id)
    
    def get_likes_count(self, post_id: int) -> int:
        return PostLikeModel.objects.filter(post_id=post_id).count()

    def get_users_who_liked_post(self, post_id: int) -> list[int]:
        return list(PostLikeModel.objects.filter(post_id=post_id).values_list('user_id', flat=True))