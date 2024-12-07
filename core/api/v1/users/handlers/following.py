# core\api\v1\posts\handlers.py
from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)

from core.api.filters import (
    PaginationIn,
    PaginationOut,
)
from core.api.schemas import (
    ApiResponce,
    ListPaginatedResponce,
)
from core.api.v1.users.filters import UserFilters
from core.api.v1.users.handlers.auth import AuthBearer
from core.api.v1.users.schemas.schemas import (
    FollowErrorSchema,
    FollowInSchema,
    FollowOutSchema,
    UnfollowOutSchema,
    UserSchema,
)
from core.apps.users.filters.users import UserFilters as UserFiltersEntity
from core.apps.users.services.follow import BaseFollowUserService
from core.project.containers import get_container


router = Router(tags=['Follow Users'], auth=AuthBearer())


@router.delete("unfollow/{following_id}", response=ApiResponce[UnfollowOutSchema], operation_id='delete_follow')
def delete_following(
    request,
    schema: Query[FollowInSchema]
) -> ApiResponce[UnfollowOutSchema]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    success = service.delete_following(
        follower_id=request.user.id,
        following_id=schema.following_id,
    )
    if not success:
        return ApiResponce(
            errors=FollowErrorSchema(
                message=f'Failed to unfollow from {schema.following_id}',
            ),
        )
    return ApiResponce(
        data=UnfollowOutSchema(
            message=f'You are unfollow from {schema.following_id} successfully',
        ),
    )


@router.post("/follow", response=ApiResponce[FollowOutSchema], operation_id='create_follow')
def create_following(
    request,
    schema: Query[FollowInSchema],
) -> ApiResponce[FollowOutSchema]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    following = service.create_following(
        follower_id=request.user.id,
        following_id=schema.following_id,
    )
    if not following:
        return ApiResponce(
            errors=FollowErrorSchema(
                message='Failed to create following',
            ),
        )

    return ApiResponce(
        data=FollowOutSchema(
            id=following.id,
            follower_id=following.follower_id,
            following_id=following.following_id,
            created_at=following.created_at,
        ),
    )


@router.get("{user_id}/followers", response=ApiResponce[ListPaginatedResponce[UserSchema]], operation_id='get_followers')
def get_followers_handler(
    request: HttpRequest,
    user_id: int,
    filters: Query[UserFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponce[ListPaginatedResponce[UserSchema]]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    user_list = service.get_user_followers(
        filters=UserFiltersEntity(search=filters.search),
        pagination=pagination_in,
        user_id=user_id,
    )
    user_count = service.get_user_followers_count(user_id=user_id)
    items = [UserSchema.from_entity(obj) for obj in user_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=user_count,
    )
    return ApiResponce(
        data=ListPaginatedResponce(items=items, pagination=pagination_out),
    )


@router.get("{user_id}/followings", response=ApiResponce[ListPaginatedResponce[UserSchema]], operation_id='get_followings')
def get_user_followings(
    request: HttpRequest,
    user_id: int,
    filters: Query[UserFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponce[ListPaginatedResponce[UserSchema]]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    user_list = service.get_user_following(
        filters=UserFiltersEntity(search=filters.search),
        pagination=pagination_in,
        user_id=user_id,
    )
    user_count = service.get_user_following_count(user_id=user_id)
    items = [UserSchema.from_entity(obj) for obj in user_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=user_count,
    )
    return ApiResponce(
        data=ListPaginatedResponce(items=items, pagination=pagination_out),
    )
