#core\apps\posts\services\posts.py
from abc import ABC, abstractmethod
from typing import Iterable

from core.apps.posts.entities.posts import Post
from core.apps.posts.models import Post as PostModel


class BasePostService(ABC):
    @abstractmethod
    def get_post_list(self) -> Iterable[Post]:
        ...
    
    @abstractmethod
    def get_post_count(self) -> int:
        ...

class ORMPostService(BasePostService):
    def get_post_list(self) -> Iterable[Post]:
        qs = PostModel.objects.filter()
        return [post.to_entity() for post in qs]
    
    def get_post_count(self) -> int:
        return PostModel.objects.filter().count()