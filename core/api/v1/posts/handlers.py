# core\api\v1\posts\handlers.py
from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError

from core.api.filters import PaginationIn
from core.api.schemas import (
    ApiResponce,
    ListPaginatedResponce,
    PaginationOut,
)
from core.api.v1.posts.filters import PostFilters
from core.api.v1.posts.schemas import (
    CreatePostSchema,
    PostInSchema,
    PostOutSchema,
    PostSchema,
)
from core.api.v1.users.handlers.auth import AuthBearer
from core.apps.common.exception import ServiceException
from core.apps.posts.filters.posts import PostFilters as PostFiltersEntity
from core.apps.posts.services.post_likes import BasePostLikeService
from core.apps.posts.services.posts import BasePostService
from core.apps.posts.use_cases.posts.create import CreatePostUseCase
from core.project.containers import get_container


router = Router(tags=['Posts'], auth=AuthBearer())


@router.get('', response=ApiResponce[ListPaginatedResponce[PostSchema]])
def get_post_list_handler(
    request: HttpRequest,
    filters: Query[PostFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponce[ListPaginatedResponce[PostSchema]]:
    container = get_container()
    service: BasePostService = container.resolve(BasePostService)
    post_list = service.get_post_list(filters=PostFiltersEntity(search=filters.search), pagination=pagination_in)
    post_count = service.get_post_count(filters=filters)
    items = [PostSchema.from_entity(obj) for obj in post_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=post_count,
    )
    return ApiResponce(
        data=ListPaginatedResponce(items=items, pagination=pagination_out),
    )

@router.post('post', response=ApiResponce[PostSchema], operation_id='createPost')
def create_comment(
    request: HttpRequest,
    schema: CreatePostSchema,
) -> ApiResponce[PostSchema]:
    container = get_container()
    use_case = container.resolve(CreatePostUseCase)

    try:
        result = use_case.execute(
            user_id=request.user.id,
            post=schema.to_entity(),
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)

    return ApiResponce(
        data=PostSchema.from_entity(result),
    )

@router.delete('{post_id}/delete', response=ApiResponce[PostOutSchema], operation_id='deletePost')
def del_post_handler(request: HttpRequest, schema: Query[PostInSchema]) -> ApiResponce[PostOutSchema]:
    container = get_container()
    service: BasePostService = container.resolve(BasePostService)
    service.delete_post(post_id=schema.post_id, user_id=request.user.id)
    return ApiResponce(
        data=PostOutSchema(
            message=f'User {request.user.id} deleted post {schema.post_id}',
        ),
    )


# Helper to get a Like's service
def get_post_like_service() -> BasePostLikeService:
    container = get_container()
    return container.resolve(BasePostLikeService)


@router.post('{post_id}/like', response=ApiResponce[PostOutSchema], operation_id='likePost')
def like_post_handler(request: HttpRequest, schema: Query[PostInSchema]) -> ApiResponce[PostOutSchema]:
    """Like post."""
    service = get_post_like_service()
    try:
        service.add_like_to_post(post_id=schema.post_id, user_id=request.user.id)
        return ApiResponce(
            data=PostOutSchema(
                message=f'User {request.user.id} liked post {schema.post_id}',
            ),
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)


@router.delete('{post_id}/unlike', response=ApiResponce[PostOutSchema], operation_id='unlikePost')
def unlike_post_handler(request: HttpRequest, schema: Query[PostInSchema]) -> ApiResponce[PostOutSchema]:
    """Removing like."""
    service = get_post_like_service()
    try:
        service.delete_like_from_post(post_id=schema.post_id, user_id=request.user.id)
        return ApiResponce(
            data=PostOutSchema(
                message=f'User {request.user.id} unliked post {schema.post_id}',
            ),
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)


@router.get('{post_id}/likes/count', response=ApiResponce[int], operation_id='getPostLikesCount')
def get_post_likes_count(request: HttpRequest, post_id: int) -> ApiResponce[int]:
    """Get the number of likes for fasting."""
    service = get_post_like_service()
    try:
        count = service.get_likes_count(post_id=post_id)
        return ApiResponce(data=count)
    except ServiceException as e:
        raise HttpError(status_code=404, message=e.message)


@router.get('{post_id}/likes/users', response=ApiResponce[list[int]], operation_id='getPostLikesUsers')
def get_post_likes_users(request: HttpRequest, post_id: int) -> ApiResponce[list[int]]:
    """Get a list of users who like post."""
    service = get_post_like_service()
    try:
        user_ids = service.get_users_who_liked_post(post_id=post_id)
        return ApiResponce(data=user_ids)
    except ServiceException as e:
        raise HttpError(status_code=404, message=e.message)
