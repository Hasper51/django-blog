from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from datetime import (
    datetime,
    timezone,
)
from typing import (
    Optional,
    Tuple,
)

from django.conf import settings
from django.contrib.auth import get_user_model

import jwt

# from django.contrib.auth.hashers import check_password
# from core.apps.users.models import User
from core.apps.users.services.codes import BaseCodeService
from core.apps.users.services.senders import BaseSenderService
from core.apps.users.services.users import BaseUserService


User = get_user_model()

# TODO: выпилить бизнес логику и перенести в use case


@dataclass(eq=False)
class BaseAuthService(ABC):
    user_service: BaseUserService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def authorize(self, email: str):
        ...

    @abstractmethod
    def register(self, email: str, username: str, password: str, first_name: str, last_name: str):
        ...

    @abstractmethod
    def confirm(self, code: str, email: str):
        ...

    @abstractmethod
    def send_verification_code(self, email: str):
        ...

    @abstractmethod
    def create_token(self, user_id: int) -> Tuple[str, str]:
        ...

    @abstractmethod
    def verify_token(self, token: str) -> Optional[int]:
        ...

    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        ...

    @abstractmethod
    def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        ...


class AuthService(BaseAuthService):
    def register(self, email: str, username: str, password: str, first_name: str, last_name: str):
        user = self.user_service.create_user(email, username, password, first_name, last_name)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def authorize(self, email: str):
        user = self.user_service.get(email)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def send_verification_code(self, email: str):
        user = self.user_service.get(email)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def confirm(self, code: str, email: str):
        user = self.user_service.get(email)
        self.codes_service.validate_code(code, user)
        self.user_service.verify_email(email)

    # JWT authentication
    def create_token(self, user_id: int) -> Tuple[str, str]:
        """Создает пару access и refresh токенов."""
        access_payload = {
            'sub': str(user_id),
            'exp': datetime.now(timezone.utc) + settings.JWT_AUTH['ACCESS_TOKEN_LIFETIME'],
            'type': 'access',
        }
        access_token = jwt.encode(
            access_payload,
            settings.JWT_AUTH['SECRET_KEY'],
            algorithm=settings.JWT_AUTH['ALGORITHM'],
        )
        refresh_payload = {
            'sub': str(user_id),
            'exp': datetime.now(timezone.utc) + settings.JWT_AUTH['REFRESH_TOKEN_LIFETIME'],
            'type': 'refresh',
        }
        refresh_token = jwt.encode(
            refresh_payload,
            settings.JWT_AUTH['SECRET_KEY'],
            algorithm=settings.JWT_AUTH['ALGORITHM'],
        )
        return access_token, refresh_token

    def verify_token(self, token: str) -> Optional[int]:
        """Проверяет JWT токен и возвращает ID пользователя."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_AUTH['SECRET_KEY'],
                algorithms=[settings.JWT_AUTH['ALGORITHM']],
            )
            if payload['type'] == 'access':
                return int(payload['sub'])
            elif payload['type'] == 'refresh':
                return int(payload['sub'])
            else:
                raise f"Unknown token type: {payload['type']}"
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.PyJWTError as e:
            raise jwt.PyJWTError(f"JWT Error: {str(e)}")

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Аутентифицирует пользователя по email и паролю."""
        try:
            # user = self.user_service.get(email)
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Создает новую пару токенов используя refresh token."""
        user_id = self.verify_token(refresh_token)
        if user_id:
            return self.create_token(user_id)
        return None
