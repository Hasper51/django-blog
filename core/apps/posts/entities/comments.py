from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.posts.entities.posts import Post
from core.apps.users.entities import User


@dataclass
class Comment:
    id: int | None = field(default=None, kw_only=True) # noqa
    user: User | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    post: Post | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    text: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = field(default=None)
