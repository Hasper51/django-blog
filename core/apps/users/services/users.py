from abc import (
    ABC,
    abstractmethod,
)
from uuid import uuid4

from core.apps.users.entities import User
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


class ORMUserService(BaseUserService):
    def get_or_create(self, email: str) -> User:
        user_dto, _ = UserModel.objects.get_or_create(email=email)
        return user_dto.to_entity()

    def get(self, email: str) -> User:
        user_dto = UserModel.objects.get(email=email)
        return user_dto.to_entity()

    def generate_token(self, user: User) -> str:
        new_token = str(uuid4())
        UserModel.objects.filter(email=user.email).update(token=new_token)
        return new_token
