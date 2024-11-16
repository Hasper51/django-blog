# core\apps\posts\entities\posts.py
from dataclasses import dataclass
from datetime import datetime


"""
entities это бизнес сущности, здесь только те поля которые исползуются бизнесом
с помошью entities мы общаемся с бизнесом
"""


@dataclass
class Post:
    id: int # noqa
    image: str
    caption: str
    user: str
    created_at: datetime
    updated_at: datetime
