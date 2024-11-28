from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.posts.entities.posts import Post
from core.apps.users.entities import User


@dataclass
class PostLike:
    id: int | None = field(default=None, kw_only=True) # noqa
    post_id: int
    user_id: int
    created_at: datetime = field(default=datetime.now)

    @classmethod
    def from_model(cls, model_instance) -> 'PostLike':
        """Creates a dataclass instance from a Django model instance."""
        return cls(
            id=model_instance.id,
            post_id=model_instance.post_id,
            user_id=model_instance.user_id,
            created_at=model_instance.created_at,
        )