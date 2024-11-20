from abc import (
    ABC,
    abstractmethod,
)

from core.apps.posts.entities.comments import Comment as CommentEntity
from core.apps.posts.entities.posts import Post as PostEntity
from core.apps.posts.exeptions.comment import CommentNotFound
from core.apps.posts.models import Comment as CommentModel
from core.apps.users.entities import User as UserEntity


class BaseCommentService(ABC):
    @abstractmethod
    def save_comment(
        self,
        user: UserEntity,
        post: PostEntity,
        comment: CommentEntity,
    ) -> CommentEntity:
        ...
    
    @abstractmethod
    def delete_comment(
        self,
        user: UserEntity,
        post: PostEntity,
        comment: CommentEntity,
    ) -> CommentEntity:
        ...

    @abstractmethod
    def get_by_id(self, comment_id: int) -> CommentEntity: ...

class ORMCommentService(BaseCommentService):
    def save_comment(
        self,
        user: UserEntity,
        post: PostEntity,
        comment: CommentEntity,
    ) -> CommentEntity:
        comment_dto: CommentModel = CommentModel.from_entity(
            comment=comment,
            post=post,
            user=user,
        )
        comment_dto.save()
        
        return comment_dto.to_entity()

    def delete_comment(
        self,
        user: UserEntity,
        post: PostEntity,
        comment: CommentEntity,
    ) -> CommentEntity:
        comment_dto: CommentModel = CommentModel.from_entity(
            comment=comment,
            post=post,
            user=user,
        )
        comment_dto.delete()
        
        return comment_dto.to_entity()

    def get_by_id(self, comment_id: int) -> CommentEntity:
        try:
            comment_dto = CommentModel.objects.get(id=comment_id)
        except CommentModel.DoesNotExist:
            raise CommentNotFound(comment_id=comment_id)

        return comment_dto.to_entity()
        