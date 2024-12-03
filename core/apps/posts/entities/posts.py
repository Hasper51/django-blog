# core\apps\posts\entities\posts.py
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.users.entities import User


"""
entities это бизнес сущности, здесь только те поля которые исползуются бизнесом
с помошью entities мы общаемся с бизнесом
"""


@dataclass
class Post:
    id: int | None = field(default=None, kw_only=True) # noqa
    image: str = field(default='')
    caption: str = field(default='')
    user: User | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = field(default=None)
