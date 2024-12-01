from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class User:
    id: int | None = field(default=None, kw_only=True) # noqa
    username: str
    email: str
    date_joined: datetime


@dataclass
class Following:
    id: int | None = field(default=None, kw_only=True) # noqa
    follower_id: int
    following_id: int
    created_at: datetime
