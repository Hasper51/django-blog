from typing import List
from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError

from core.api.schemas import ApiResponce
from core.api.v1.comments.schemas import (
    CommentInSchema,
    CommentLikeInSchema,
    CommentLikeOutSchema,
    CommentOutSchema,
    CommentListSchema,
)
from core.api.v1.users.handlers.auth import AuthBearer
from core.apps.common.exception import ServiceException
from core.apps.posts.services.comment_likes import BaseCommentLikeService
from core.apps.posts.services.comments import BaseCommentService
from core.apps.posts.use_cases.comments.create import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
)
from core.project.containers import get_container


router = Router(tags=['Comments'], auth=AuthBearer())

@router.get('{post_id}/comments', response=ApiResponce[CommentListSchema], operation_id='getComments')
def get_comments(
    request: HttpRequest,
    post_id: int,
) -> ApiResponce[CommentListSchema]:
    container = get_container()
    service = container.resolve(BaseCommentService)

    try:
        comments = service.get_comments_by_post(post_id=post_id)
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)

    return ApiResponce(
        data=CommentListSchema(list(map(CommentOutSchema.from_entity, comments)))
    )
@router.post('{post_id}/comment', response=ApiResponce[CommentOutSchema], operation_id='createComment')
def create_comment(
    request: HttpRequest,
    post_id: int,
    schema: CommentInSchema,
    token: str,
) -> ApiResponce[CommentOutSchema]:
    container = get_container()
    use_case = container.resolve(CreateCommentUseCase)

    try:
        result = use_case.execute(
            user_token=token,
            post_id=post_id,
            comment=schema.to_entity(),
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)

    return ApiResponce(
        data=CommentOutSchema.from_entity(result),
    )


@router.delete('{post_id}/comment/{comment_id}/delete', response=ApiResponce[CommentOutSchema], operation_id='deleteComment')
def delete_comment(
    request: HttpRequest,
    post_id: int,
    comment_id: int,
    token: str,
) -> ApiResponce[CommentOutSchema]:
    container = get_container()
    use_case = container.resolve(DeleteCommentUseCase)

    try:
        result = use_case.execute(
            user_token=token,
            post_id=post_id,
            comment_id=comment_id,
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)

    return ApiResponce(
        data=CommentOutSchema.from_entity(result),
    )


# Helper to get a Like's service
def get_comment_like_service() -> BaseCommentLikeService:
    container = get_container()
    return container.resolve(BaseCommentLikeService)


@router.post('{post_id}/comment/{comment_id}/like', response=ApiResponce[CommentLikeOutSchema], operation_id='likeComment')
def like_comment_handler(request: HttpRequest, schema: Query[CommentLikeInSchema]) -> ApiResponce[CommentLikeOutSchema]:
    """Like post."""
    service = get_comment_like_service()
    try:
        service.add_like_to_comment(comment_id=schema.comment_id, user_id=schema.user_id)
        return ApiResponce(
            data=CommentLikeOutSchema(
                message=f'User {schema.user_id} liked comment {schema.comment_id}',
            ),
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)


@router.delete('{post_id}/comment/{comment_id}/unlike', response=ApiResponce[CommentLikeOutSchema], operation_id='unlikeComment')
def unlike_comment_handler(request: HttpRequest, schema: Query[CommentLikeInSchema]) -> ApiResponce[CommentLikeOutSchema]:
    """Removing like."""
    service = get_comment_like_service()
    try:
        service.delete_like_from_comment(comment_id=schema.comment_id, user_id=schema.user_id)
        return ApiResponce(
            data=CommentLikeOutSchema(
                message=f'User {schema.user_id} unliked comment {schema.comment_id}',
            ),
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)


@router.get('{post_id}/comment/{comment_id}/likes/count', response=ApiResponce[int], operation_id='getCommentLikesCount')
def get_comment_likes_count(request: HttpRequest, comment_id: int) -> ApiResponce[int]:
    """Get the number of likes for fasting."""
    service = get_comment_like_service()
    try:
        count = service.get_likes_count(comment_id=comment_id)
        return ApiResponce(data=count)
    except ServiceException as e:
        raise HttpError(status_code=404, message=e.message)
