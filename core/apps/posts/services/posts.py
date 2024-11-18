# core\apps\posts\services\posts.py
from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.posts.entities.posts import Post
from core.apps.posts.exeptions.posts import PostNotFound
from core.apps.posts.filters.posts import PostFilters
from core.apps.posts.models import Post as PostModel


'''Сервисы принимают entity-объекты и возвращают entity-объекты
'''


class BasePostService(ABC):
    @abstractmethod
    def get_post_list(
        self, filters: PostFilters, pagination: PaginationIn,
    ) -> Iterable[Post]: ...

    @abstractmethod
    def get_post_count(self, filters: PostFilters) -> int: ...

    @abstractmethod
    def get_by_id(self, post_id: int) -> int: ...


class ORMPostService(BasePostService):
    def _build_post_query(self, filters: PostFilters) -> Q:
        query = Q()  # может быть фильтр в скобках

        if filters.search is not None:
            query &= Q(caption__icontains=filters.search)

        return query

    def get_post_list(
        self, filters: PostFilters, pagination: PaginationIn,
    ) -> Iterable[Post]:
        query = self._build_post_query(filters)
        qs = PostModel.objects.filter(query)[
            pagination.offset:pagination.offset+pagination.limit
        ]

        return [post.to_entity() for post in qs]

    def get_post_count(self, filters: PostFilters) -> int:
        query = self._build_post_query(filters)

        return PostModel.objects.filter(query).count()

    def get_by_id(self, post_id: int) -> int:
        try:
            post_dto = PostModel.objects.get(pk=post_id)
        except PostModel.DoesNotExist:
            raise PostNotFound(post_id=post_id)

        return post_dto.to_entity()
