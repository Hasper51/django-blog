from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Iterable,
    List,
    Optional,
    Tuple,
)

from django.core.cache import cache
from django.db.models import (
    Max,
    Q,
)

from core.api.filters import PaginationIn
from core.apps.users.entities import (
    Following as FollowingEntity,
    User as UserEntity,
)
from core.apps.users.filters.users import UserFilters
from core.apps.users.models import (
    Following as FollowingModel,
    User as UserModel,
)


class BaseFollowUserService(ABC):
    @abstractmethod
    def create_following(
        self,
        follower_id: int,
        following_id: int,
    ) -> Optional[FollowingEntity]:
        pass

    @abstractmethod
    def delete_following(
        self,
        follower_id: int,
        following_id: int,
    ) -> bool:
        pass

    @abstractmethod
    def get_user_followers(
        self,
        user_id: int,
        page: int,
    ) -> Tuple[List[FollowingEntity], int]:
        pass

    @abstractmethod
    def get_user_followers_count(self, user_id: int) -> int:
        ...

    @abstractmethod
    def get_user_following(
        self,
        user_id: int,
        page: int,
    ) -> Tuple[List[FollowingEntity], int]:
        pass

    @abstractmethod
    def get_user_followings_count(self, user_id: int) -> int:
        ...


class ORMFollowUserService(BaseFollowUserService):
    CACHE_TTL = 3600  # 1 hour
    FOLLOWERS_PER_PAGE = 50

    def _build_user_query(
        self,
        filters: UserFilters,
    ) -> Q:
        query = Q()  # может быть фильтр в скобках

        if filters.search is not None:
            query &= Q(username__icontains=filters.search)

        return query

    def _get_cache_key(self, user_id: int, list_type: str) -> str:
        return f"user:{user_id}:{list_type}"

    def create_following(
        self,
        follower_id: int,
        following_id: int,
    ) -> Optional[FollowingEntity]:
        if follower_id == following_id:
            raise ValueError("Users cannot follow themselves")

        try:
            # Check if users exist
            if not UserModel.objects.filter(id__in=[follower_id, following_id]).count() == 2:
                raise ValueError("One or both users not found")

            following = FollowingModel.objects.create(
                follower_id=follower_id,
                following_id=following_id,
            )

            # Invalidate cache
            cache_keys = [
                self._get_cache_key(follower_id, "following"),
                self._get_cache_key(following_id, "followers"),
            ]
            cache.delete_many(cache_keys)

            return following.to_entity()
        except Exception as e:
            # Log error here
            return None

    def delete_following(
        self,
        follower_id: int,
        following_id: int,
    ) -> bool:
        try:
            deleted = FollowingModel.objects.filter(
                follower_id=follower_id,
                following_id=following_id,
            ).delete()

            if deleted[0] > 0:
                # Invalidate cache
                cache_keys = [
                    self._get_cache_key(follower_id, "following"),
                    self._get_cache_key(following_id, "followers"),
                ]
                cache.delete_many(cache_keys)
                return True
            return False
            # return True
        except Exception as e:
            # Log error here
            return False

    def get_user_followers(
        self,
        filters: UserFilters,
        pagination: PaginationIn,
        user_id: int,
    ) -> Iterable[UserEntity]:
        query = self._build_user_query(filters)
        follower_qs = FollowingModel.objects.filter(following_id=user_id).values_list('follower_id', flat=True)
        user_qs = UserModel.objects.filter(Q(id__in=follower_qs) & Q(query))\
            .annotate(last_followed=Max('following__created_at'))\
            .order_by('-last_followed')[
                pagination.offset:pagination.offset+pagination.limit
            ]
        return [user.to_entity() for user in user_qs]

    def get_user_followers_count(self, user_id: int) -> int:
        count = FollowingModel.objects.filter(following_id=user_id).count()
        return count

    def get_user_following(
        self,
        filters: UserFilters,
        pagination: PaginationIn,
        user_id: int,
    ) -> Iterable[UserEntity]:
        query = self._build_user_query(filters)
        following_qs = FollowingModel.objects.filter(follower_id=user_id).values_list('following_id', flat=True)
        user_qs = UserModel.objects.filter(Q(id__in=following_qs) & Q(query))\
            .annotate(last_followed=Max('followers__created_at'))\
            .order_by('-last_followed')[
                pagination.offset:pagination.offset+pagination.limit
            ]
        return [user.to_entity() for user in user_qs]

    def get_user_followings_count(self, user_id: int) -> int:
        count = FollowingModel.objects.filter(follower_id=user_id).count()
        return count
