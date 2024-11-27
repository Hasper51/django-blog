# core\api\v1\posts\handlers.py
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.middleware.csrf import get_token
from ninja import Router
from ninja.errors import HttpError
from ninja.security import django_auth

from core.api.schemas import ApiResponce
from core.api.v1.users.schemas import (
    AuthOutSchema,
    SignInSchema,
)
from core.apps.users.services.auth import BaseAuthService
from core.project.containers import get_container

from . import schemas


router = Router(tags=['Login'])


@router.get("/set-csrf-token")
def get_csrf_token(request):
    return {"csrftoken": get_token(request)}

# TODO если пользователь с неверефицированным email, пробует зайти с помощи email, а не username, то user = None. Нужно исправить
@router.post("/login", response=ApiResponce[AuthOutSchema], operation_id='login')
def login_view(request, schema: SignInSchema) -> ApiResponce[AuthOutSchema]:
    user = authenticate(request, username=schema.email, password=schema.password)
    
    if user is not None:
        if user.email_verified:
            login(request, user)
            return ApiResponce(data=AuthOutSchema(message="Logged in"))
        else:
            container = get_container()
            service: BaseAuthService = container.resolve(BaseAuthService)
            service.send_verification_code(user.email)
            return ApiResponce(data=AuthOutSchema(message="Failed to login, verify your email"))
    return ApiResponce(data=AuthOutSchema(message="Failed to login"))


@router.post("/logout", auth=django_auth)
def logout_view(request):
    try:
        logout(request)
        return {"message": "Logged out"}
    except Exception as e:
        raise HttpError(
            status_code=403,
            message=str(e),
        )


@router.get("/user", auth=django_auth)
def user(request):
    secret_fact = (
        "The moment one gives close attention to any thing, even a blade of grass",
        "it becomes a mysterious, awesome, indescribably magnificent world in itself.",
    )
    return {
        "username": request.user.username,
        "email": request.user.email,
        "secret_fact": secret_fact,
    }


@router.post("/register")
def register(request, schema: schemas.SignUpSchema) -> ApiResponce[AuthOutSchema]:
    container = get_container()
    service: BaseAuthService = container.resolve(BaseAuthService)

    service.register(schema.email, schema.username, schema.password)
    return ApiResponce(
        data=AuthOutSchema(
            message=f'Code is sent to {schema.email}',
        ),
    )
