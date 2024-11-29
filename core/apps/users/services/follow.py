from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
    Tuple,
)

from django.core.cache import cache
from django.core.paginator import Paginator

from core.apps.users.entities import Following as FollowingEntity
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
    def get_user_following(
        self,
        user_id: int,
        page: int,
    ) -> Tuple[List[FollowingEntity], int]:
        pass


class ORMFollowUserService(BaseFollowUserService):
    CACHE_TTL = 3600  # 1 hour
    FOLLOWERS_PER_PAGE = 50

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
        user_id: int,
        page: int = 1,
    ) -> Tuple[List[FollowingEntity], int]:
        cache_key = self._get_cache_key(user_id, f"followers:page:{page}")
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        queryset = FollowingModel.objects.filter(following_id=user_id)
        paginator = Paginator(queryset, self.FOLLOWERS_PER_PAGE)
        page_obj = paginator.get_page(page)

        followers = [
            following.to_entity()
            for following in page_obj
        ]

        result = (followers, paginator.count)
        cache.set(cache_key, result, self.CACHE_TTL)
        return result

    def get_user_following(
        self,
        user_id: int,
        page: int = 1,
    ) -> Tuple[List[FollowingEntity], int]:
        cache_key = self._get_cache_key(user_id, f"following:page:{page}")
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        queryset = FollowingModel.objects.filter(follower_id=user_id)
        paginator = Paginator(queryset, self.FOLLOWERS_PER_PAGE)
        page_obj = paginator.get_page(page)

        following = [
            following.to_entity()
            for following in page_obj
        ]

        result = (following, paginator.count)
        cache.set(cache_key, result, self.CACHE_TTL)
        return result
