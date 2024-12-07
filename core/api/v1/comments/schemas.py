from datetime import datetime

from pydantic import BaseModel

from core.apps.posts.entities.comments import Comment as CommentEntity


class CommentInSchema(BaseModel):
    text: str

    def to_entity(self):
        return CommentEntity(
            text=self.text,
        )


class CreateCommentSchema(BaseModel):
    post_id: int
    user_id: int
    comment: CommentInSchema


class CommentOutSchema(CommentInSchema):
    id: int # noqa
    username: str
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, comment: CommentEntity) -> 'CommentOutSchema':
        return cls(
            id=comment.id,
            text=comment.text,
            username=comment.user.username,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


CommentListSchema = list[CommentOutSchema]


class CommentLikeInSchema(BaseModel):
    comment_id: int


class CommentLikeOutSchema(BaseModel):
    message: str
