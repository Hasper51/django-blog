from abc import ABC, abstractmethod
import random

from django.core.cache import cache

from core.apps.users.entities import UserEntity
from core.apps.users.exceptions.codes import CodeNotFoundException, CodesNotEqualException


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, user: UserEntity) -> str:
        ...

    @abstractmethod
    def validate_code(self, code: str, user: UserEntity) -> None:
        ...

class DjangoCacheCodeService(BaseCodeService):
    def generate_code(self, user: UserEntity) -> str:
        code = ''.join(random.choices('0123456789', k=6))
        
        # Store the code in the cache with a unique key
        # This example uses Django's cache framework, but you can use any caching library you prefer

        cache.set(user.email, code) # Can set parameter: timeout=60
        return code
    
    def validate_code(self, code: str, user: UserEntity) -> None:
        cached_code = cache.get(user.email)

        if cached_code is None:
            raise CodeNotFoundException(code=code)
        
        if cached_code != code:
            raise CodesNotEqualException(
                code=code,
                cached_code=cached_code,
                user_email=user.email
            )

        cache.delete(user.email)