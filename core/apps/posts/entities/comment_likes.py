from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class CommentLike:
    id: int | None = field(default=None, kw_only=True) # noqa
    comment_id: int
    user_id: int
    created_at: datetime = field(default=datetime.now)
