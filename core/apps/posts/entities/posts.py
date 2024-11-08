#core\apps\posts\entities\posts.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    id: int
    image: str
    caption: str
    author: str
    created_at: datetime
    updated_at: datetime