from abc import ABC, abstractmethod
from uuid import uuid4

from core.apps.users.entities import UserEntity
from core.apps.users.models import User as UserModel


class BaseUserService(ABC):
    @abstractmethod
    def get_or_create(self, email: str) -> UserEntity:
        ...

    @abstractmethod
    def generate_token(self, user: UserEntity) -> str:
        ...
    
    @abstractmethod
    def get(self, email: str) -> UserEntity:
        ...


class ORMUserService(BaseUserService):
    def get_or_create(self, email: str) -> UserEntity:
        user_dto, _ = UserModel.objects.get_or_create(email=email)
        return user_dto.to_entity()
    
    def get(self, email: str) -> UserEntity:
        user_dto = UserModel.objects.get(email=email)
        return user_dto.to_entity()
    
    def generate_token(self, user: UserEntity) -> str:
        new_token = str(uuid4())
        UserModel.objects.filter(email=user.email).update(token=new_token)
        return new_token