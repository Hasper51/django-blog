from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class PostLike:
    id: int | None = field(default=None, kw_only=True) # noqa
    post_id: int
    user_id: int
    created_at: datetime = field(default=datetime.now)
