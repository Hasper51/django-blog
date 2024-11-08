# core\apps\posts\services\posts.py
from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.posts.filters import PostFilters
from core.apps.posts.entities.posts import Post
from core.apps.posts.models import Post as PostModel


class BasePostService(ABC):
    @abstractmethod
    def get_post_list(
        self, filters: PostFilters, pagination: PaginationIn,
    ) -> Iterable[Post]: ...

    @abstractmethod
    def get_post_count(self, filters: PostFilters) -> int: ...


class ORMPostService(BasePostService):
    def _build_post_query(self, filters: PostFilters) -> Q:
        query = Q()  # фильтр в скобках

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
