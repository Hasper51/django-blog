from dataclasses import dataclass, field

from core.apps.common.enums import EntityStatus
from core.apps.posts.entities.posts import Post
from core.apps.users.entities import User


@dataclass
class Comment:
    user: User | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    post: Post | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    text: str = field(default='')
