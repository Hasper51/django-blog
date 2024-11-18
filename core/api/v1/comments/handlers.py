from django.http import HttpRequest
from ninja import Header, Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponce
from core.api.v1.comments.schemas import CommentInSchema, CommentOutSchema
from core.apps.common.exception import ServiceException
from core.apps.posts.use_cases.comments.create import CreateCommentUseCase
from core.project.containers import get_container

from ninja.security import django_auth

router = Router(tags=['Comments'])


@router.post('{post_id}/comment', response=ApiResponce[CommentOutSchema], operation_id='createComment', auth=django_auth)
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
            comment=schema.to_entity()
        )
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)

    return ApiResponce(
        data=CommentOutSchema.from_entity(result)
    )
