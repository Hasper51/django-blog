# core\api\v1\posts\schemas.py
from datetime import datetime

from ninja import Schema

from pydantic import BaseModel

from core.apps.posts.entities.posts import Post as PostEntity


"""
схема это как API должен видеть модель
с помошью схемы мы общаемся с интерфейсами
"""


class PostSchema(BaseModel):
    id: int  # noqa
    image: str
    caption: str
    user: int
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: PostEntity) -> 'PostSchema':
        return PostSchema(
            id=entity.id,
            image=entity.image,
            caption=entity.caption,
            user=entity.user,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self):
        return PostEntity(
            image=self.image,
            caption=self.caption,
        )


PostListSchema = list[PostSchema]


class CreatePostSchema(Schema):
    image: str
    caption: str
    
    def to_entity(self):
        return PostEntity(
            image=self.image,
            caption=self.caption,
        )


class PostInSchema(BaseModel):
    post_id: int
    user_id: int


class PostOutSchema(BaseModel):
    message: str
