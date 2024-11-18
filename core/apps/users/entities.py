from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class User:
    id: int | None = field(default=None, kw_only=True) # noqa
    email: str
    date_joined: datetime
