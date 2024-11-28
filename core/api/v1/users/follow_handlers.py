# core\api\v1\posts\handlers.py
from typing import Optional
from django.http import HttpRequest
from ninja import Path, Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponce
from core.api.v1.users.schemas import (
    AuthInSchema,
    AuthOutSchema,
    FollowCreateSchema,
    FollowErrorSchema,
    FollowOutSchema,
    TokenInSchema,
    TokenOutSchema,
    UnfollowOutSchema,
    UserFollowersOut,
)
from core.apps.common.exception import ServiceException
from core.apps.users.services.auth import BaseAuthService
from core.apps.users.services.follow import BaseFollowUserService
from core.project.containers import get_container


router = Router(tags=['Follow Users'])


@router.delete("unfollow/{following_id}", response=ApiResponce[UnfollowOutSchema], operation_id='delete_follow')
def delete_following(request, following_id: int) -> ApiResponce[UnfollowOutSchema]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    success =  service.delete_following(
        follower_id=request.user.id,
        following_id=following_id
    )
    if not success:
        return ApiResponce(
            errors=FollowErrorSchema(
                message=f'Failed to unfollow',
            )
        )
    return ApiResponce(
        data=UnfollowOutSchema(
            message = f'You are unfollow from {following_id} successfully'
        )
    )


@router.post("/follow", response=ApiResponce[FollowOutSchema], operation_id='create_follow')
def create_following(
    request,
    payload: FollowCreateSchema,
) -> ApiResponce[FollowOutSchema]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    following = service.create_following(
        follower_id=request.user.id,
        following_id=payload.following_id
    )
    if not following:
        return ApiResponce(
            errors=FollowErrorSchema(
                message=f'Failed to create following',
            )
        )

    return ApiResponce(
        data=FollowOutSchema(
            id=following.id,
            follower_id=following.follower_id,
            following_id=following.following_id,
            created_at=following.created_at,
        ),
    )


@router.get("/users/{user_id}/followers", response=ApiResponce[UserFollowersOut], operation_id='get_followers')
def get_followers_handler(request: HttpRequest, user_id: int = Path(...), page: int = 1) -> ApiResponce[FollowOutSchema]:
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    followers, total =  service.get_user_followers(user_id, page)
    return ApiResponce(
        data=UserFollowersOut(
            total_followers=total,
            followers=followers,
        ),
    )


@router.get("/users/{user_id}/followings", response=ApiResponce[UserFollowersOut], operation_id='get_followings')
def get_user_followings(
    request: HttpRequest,
    user_id: int = Path(...),
    page: int = 1
):
    container = get_container()
    service = container.resolve(BaseFollowUserService)
    followings, total = service.get_user_following(user_id, page)
    return ApiResponce(
        data=UserFollowersOut(
            total_followers=total,
            followers=followings,
        ),
    )