# core\api\v1\posts\handlers.py
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponce
from core.api.v1.users.handlers.auth import AuthBearer
from core.api.v1.users.schemas.jwt import (
    AuthInSchema,
    AuthOutSchema,
    TokenSchema,
    UserCreate,
    UserOut,
)
from core.api.v1.users.schemas.schemas import TokenInSchema
from core.apps.common.exception import ServiceException
from core.apps.users.services.auth import BaseAuthService
from core.project.containers import get_container


User = get_user_model()

router = Router(tags=['Users'])


@router.get("/users/me", response=ApiResponce[UserOut], auth=AuthBearer())
def get_current_user(request):
    """Получение информации о текущем пользователе."""
    user = User.objects.get(id=request.user_id)
    return ApiResponce(
        data=UserOut(
            id=user.pk,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.date_joined,
        ),
    )


@router.post('auth/login', response=ApiResponce[TokenSchema], operation_id='login')
def login_handler(request: HttpRequest, schema: AuthInSchema) -> ApiResponce[TokenSchema]:
    container = get_container()
    service: BaseAuthService = container.resolve(BaseAuthService)

    user = service.authenticate_user(
        email=schema.email,
        password=schema.password,
    )
    if not user:
        raise HttpError(
            status_code=400,
            message='Incorrect email or password',
        )
    access_token, refresh_token = service.create_token(user.id)
    return ApiResponce(
        data=TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )


@router.post('auth/confirm', response=ApiResponce[AuthOutSchema], operation_id='confirmCode')
def get_token_handler(request: HttpRequest, schema: TokenInSchema) -> ApiResponce[AuthOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)
    try:
        service.confirm(schema.code, schema.email)
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        )

    return ApiResponce(
        data=AuthOutSchema(
            message="Email is confirmed",
        ),
    )


@router.post('auth/register', response=ApiResponce[AuthOutSchema], operation_id='register')
def register_handler(request: HttpRequest, schema: UserCreate) -> ApiResponce[AuthOutSchema]:
    container = get_container()
    service: BaseAuthService = container.resolve(BaseAuthService)

    service.register(schema.email, schema.username, schema.password, schema.first_name, schema.last_name)
    return ApiResponce(
        data=AuthOutSchema(
            message=f'Code is sent to {schema.email}',
        ),
    )


@router.post('auth/refresh', response=ApiResponce[TokenSchema], operation_id='refreshToken')
def refresh_token_handler(request: HttpRequest, refresh_token: str) -> ApiResponce[TokenSchema]:
    container = get_container()
    service: BaseAuthService = container.resolve(BaseAuthService)

    new_tokens = service.refresh_tokens(refresh_token=refresh_token)

    if not new_tokens:
        raise HttpError(
            status_code=400,
            message='Invalid or expired refresh token',
        )
    access_token, refresh_token = new_tokens
    return ApiResponce(
        data=TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )
