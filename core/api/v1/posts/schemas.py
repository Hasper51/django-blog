# core\api\v1\posts\schemas.py
from datetime import datetime

from pydantic import BaseModel

from core.apps.posts.entities.posts import Post as PostEntity


"""
схема это как API должен видеть модель
с помошью схемы мы общаемся с интерфейсами
"""


class PostSchema(BaseModel):
    id: int  #noqa
    image: str
    caption: str
    author: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: PostEntity) -> 'PostSchema':
        return PostSchema(
            id=entity.id,
            image=entity.image,
            caption=entity.caption,
            author=entity.author,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


PostListSchema = list[PostSchema]
