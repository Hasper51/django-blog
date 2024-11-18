from abc import ABC, abstractmethod
from core.apps.posts.entities.comments import Comment as CommentEntity
from core.apps.posts.entities.posts import Post as PostEntity
from core.apps.posts.models import Comment as CommentModel
from core.apps.users.entities import User as UserEntity


class BaseCommentService(ABC):
    @abstractmethod
    def save_comment(
        self,
        user: UserEntity,
        post: PostEntity,
        comment: CommentEntity
    ) -> CommentEntity:
        ...


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
            user=user
        )
        comment_dto.save()
        
        return comment_dto.to_entity()

