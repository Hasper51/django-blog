from abc import (
    ABC,
    abstractmethod,
)
from uuid import uuid4

from django.core.exceptions import ValidationError

from core.apps.users.entities import User
from core.apps.users.exceptions.user import UserTokenInvalid
from core.apps.users.models import User as UserModel


class BaseUserService(ABC):
    @abstractmethod
    def get_or_create(self, email: str) -> User:
        ...

    @abstractmethod
    def generate_token(self, user: User) -> str:
        ...

    @abstractmethod
    def get(self, email: str) -> User:
        ...

    @abstractmethod
    def get_by_token(self, token: str) -> User:
        ...

    @abstractmethod
    def create_user(self, email: str, username: str, password: str) -> User:
        ...

    @abstractmethod
    def verify_email(self, email: str) -> None:
        ...


class ORMUserService(BaseUserService):
    def get_or_create(self, email: str) -> User:
        user_dto, _ = UserModel.objects.get_or_create(email=email)
        return user_dto.to_entity()

    def get(self, email: str) -> User:
        user_dto = UserModel.objects.get(email=email)
        
        def __str__(self):
            return f"User(email={self.email})"
        return user_dto.to_entity()

    def generate_token(self, user: User) -> str:
        new_token = str(uuid4())
        UserModel.objects.filter(email=user.email).update(token=new_token)
        return new_token

    def get_by_token(self, token: str) -> User:
        try:
            user_dto = UserModel.objects.get(token=token)
        except UserModel.DoesNotExist:
            raise UserTokenInvalid(token=token)

        return user_dto.to_entity()

    def create_user(self, email: str, username: str, password: str) -> User:
        if UserModel.objects.filter(username=username).exists():
            raise ValidationError("User with this username already exists")
        try:
            user_dto = UserModel.objects.create_user(
                email=email,
                username=username,
                password=password,
            )
        except Exception as e:
            raise e
        return user_dto.to_entity()

    def verify_email(self, email: str) -> None:
        UserModel.objects.filter(email=email).update(email_verified=True)
