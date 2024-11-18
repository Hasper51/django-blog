# core\api\v1\posts\handlers.py
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponce
from core.api.v1.users.schemas import (
    AuthInSchema,
    AuthOutSchema,
    TokenInSchema,
    TokenOutSchema,
)
from core.apps.common.exception import ServiceException
from core.apps.users.services.auth import BaseAuthService
from core.project.containers import get_container


router = Router(tags=['Users'])


@router.post('auth', response=ApiResponce[AuthOutSchema], operation_id='authorize')
def auth_handler(request: HttpRequest, schema: AuthInSchema) -> ApiResponce[AuthOutSchema]:
    container = get_container()
    service: BaseAuthService = container.resolve(BaseAuthService)

    service.authorize(schema.email)
    return ApiResponce(
        data=AuthOutSchema(
            message=f'Code is sent to {schema.email}',
        ),
    )


@router.post('confirm', response=ApiResponce[TokenOutSchema], operation_id='confirmCode')
def get_token_handler(request: HttpRequest, schema: TokenInSchema) -> ApiResponce[TokenOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)
    try:
        token = service.confirm(schema.code, schema.email)
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        )

    return ApiResponce(
        data=TokenOutSchema(
            token=token,
        ),
    )
