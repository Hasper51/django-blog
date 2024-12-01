from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Iterable,
    List,
)

from core.api.filters import PaginationIn
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

    @abstractmethod
    def get_comments_by_post(self, post_id: int) -> List[CommentEntity]: ...

    @abstractmethod
    def get_comment_list(
        self, post_id: int, pagination: PaginationIn,
    ) -> Iterable[CommentEntity]: ...

    @abstractmethod
    def get_comment_count(self, post_id: int) -> int: ...


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

    def get_comments_by_post(self, post_id: int) -> List[CommentEntity]:
        comment_dtos = CommentModel.objects.filter(post_id=post_id)
        return [comment_dto.to_entity() for comment_dto in comment_dtos]

    def get_comment_list(
        self,
        post_id: int,
        pagination: PaginationIn,
    ) -> Iterable[CommentEntity]:
        qs = CommentModel.objects.filter(post_id=post_id)[
            pagination.offset:pagination.offset+pagination.limit
        ]

        return [comment.to_entity() for comment in qs]

    def get_comment_count(self, post_id: int) -> int:
        return CommentModel.objects.filter(post_id=post_id).count()
